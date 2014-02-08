import logging
import traceback
from django.http import HttpResponse
from django.utils import timezone
from inflection import camelize
import sys
from tastypie.models import ApiKey
from footprint.celery import app
from footprint.common.utils.async import start_and_track_task
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.lib.functions import remove_keys, merge
from footprint.main.models import ConfigEntity
from footprint.main.utils.utils import resolve_module_attr, full_module_path

logger = logging.getLogger(__name__)

__author__ = 'calthorpe'


def post_save_publishing(signal_path, config_entity, user, **kwargs):
    api_key = ApiKey.objects.get(user=user).key

    # Pass the arguments to the task and run via celery. Note that kwargs is being treated
    # as a dict here and passed along
    instance_id = kwargs['instance'].id
    instance_class = full_module_path(kwargs['instance'].__class__)
    # Sanity check to make sure this works, since it sometimes fails in the celery task
    try:
        instance = kwargs.get('instance', resolve_module_attr(instance_class).objects.get(id=instance_id))
        instance_key = kwargs['instance_key'] if kwargs.get('instance_key', None) else instance.key
        logger.info("\tPost save instance %s of class %s and id %s" % (instance_key, instance_class, instance_id))
    except Exception, e:
        logger.error("What the heck is going on? Unable to resolve instance of class %s and id %s" % (instance_class, instance_id))
        raise e


    job = start_and_track_task(_post_save_publishing,
                               api_key,
                               config_entity,
                               user,
                               merge(remove_keys(kwargs, ['instance']),
                                     dict(
                                         signal_path=signal_path,
                                         instance_class=instance_class,
                                         instance_id=instance_id)))
    return HttpResponse(job.hashid)


@app.task
def _post_save_publishing(job, config_entity, user, kwargs):
    """
        Runs all configured publishers via the Django signals they depend upon.
        This is done in Celery in order to support long running tasks launched from a client.
        Peer tasks are run in parallel. Dependent tasks are called after the tasks they depend on complete

    :param hash_id: Job hash id
    :param config_entity:
    :param user: The current user or None if no user is in scope
    :return:
    """

    try:
        instance = kwargs.get('instance', resolve_module_attr(kwargs['instance_class']).objects.get(id=kwargs['instance_id']))
    except Exception, e:
        # Mysteriously, sometimes Celery can't load the instance by instance_class and instance_id, even thought the instance
        # has already been saved. Try it again and then give up.
        try:
            import time
            time.sleep(0.5)
            instance = kwargs.get('instance', resolve_module_attr(kwargs['instance_class']).objects.get(id=kwargs['instance_id']))
        except Exception, e:
            raise Exception("Unable to resolve instance of class %s and id %s. Message: %s" % (kwargs['instance_class'], kwargs['instance_id'], e.message))

    updated_kwargs = merge(dict(instance=instance), remove_keys(kwargs, ['signal_path', 'instance_class', 'instance_id']))

    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()

    # The signal that we'll send to kick off dependent publishers
    # We'll alse use it to recurse on dependent signals
    signal_path = kwargs['signal_path']
    # Lookup the dependent signal paths of the signal. We'll use these to recurse
    dependent_signal_paths = kwargs['dependent_signal_paths'](signal_path)
    # We use the prefix of the signal_paths as an event name for the client
    # For example 'post_save_config_entity' becomes postSaveConfigEntity here
    # We suffix the event name with PublisherCompleted or PublisherFailed
    client_event = camelize(kwargs['signal_prefix'], False)

    # Send a message to client announcing which signal completed
    # The message sends the camelized version of the signal name
    # For instance post_save_config_entity_initial becomes postSaveConfigEntityInitial
    # where config_entity_subclass_name is the name of the subclass to make it clear to receivers in javascript what type was receved
    signal_proportion_lookup_name = signal_path.split('.')[-1]
    publisher_name = unicode(
        camelize(
            signal_proportion_lookup_name,
            False
        )
    )

    instance_key = kwargs['instance_key'] if kwargs.get('instance_key', None) else instance.key
    try:
        # TODO causing duplicate pk errors in concurrent mode
        #job.status = 'Started'
        #job.save()

        logger.debug("\tRunning handlers for signal {signal_path} for key {key}".format(
            config_entity=config_entity,
            username=user.username,
            signal_path=signal_path,
            key=instance_key))

        # Send the signal. The listening publishers will run in sequence
        resolve_module_attr(signal_path).send(sender=config_entity.__class__, **updated_kwargs)
        event = '%sPublisherCompleted' % client_event
        logger.debug("Sending message %s for signal complete %s to client with key %s" % (event, signal_proportion_lookup_name, instance_key))

        send_message_to_client(user.id, dict(
            event=event,
            job_id=str(job.hashid),
            config_entity_id=config_entity.id,
            config_entity_class_name=config_entity.__class__.__name__,
            # Send the key since the id of new instances might be meaningless to the client
            # If it hasn't updated the record's id yet
            key=instance_key,
            publisher_name=publisher_name,
            class_name=instance.__class__.__name__,
            id=instance.id,
            # Send the proportion of work that completing this signal signifies--0 to 1
            proportion=kwargs.get('signal_proportion_lookup', {}).get(signal_proportion_lookup_name, 0)
        ))

        # Find all dependent signals of this one and run each in parallel
        for dependent_signal_path in dependent_signal_paths:
            post_save_publishing(
                dependent_signal_path,
                config_entity,
                user,
                **updated_kwargs
            )
        job.status = 'Complete'

    except Exception, e:
        if kwargs.get('created'):
            # Let the instance delete itself on a post save creation error
            instance.handle_post_save_create_error()

        job.status = "Failed"
        exc_type, exc_value, exc_traceback = sys.exc_info()
        readable_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
        job.data = readable_exception
        event = '%sPublisherFailed' % client_event
        logger.debug("Sending Failed message %s for signal %s to client with key %s" % (event, signal_proportion_lookup_name, instance_key))
        send_message_to_client(user.id, dict(
            event=event,
            config_entity_id=config_entity.id,
            config_entity_class_name=config_entity.__class__.__name__,
            # Send the key since the id of new instances might be meaningless to the client
            # If it hasn't updated the record's id yet
            key=instance_key,
            class_name=instance.__class__.__name__,
            id=instance.id,
            publisher_name=publisher_name,
            trace=readable_exception)
        )
        raise Exception(readable_exception)
    finally:
        job.ended_on = timezone.now()
        job.save()
