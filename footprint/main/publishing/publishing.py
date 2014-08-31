import logging
import traceback
from celery import Task
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from inflection import camelize, humanize
import sys
from tastypie.models import ApiKey
from footprint.celery import app
from footprint.common.utils.async import start_and_track_task
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.lib.functions import remove_keys, merge
from footprint.main.utils.utils import resolve_module_attr, full_module_path

logger = logging.getLogger(__name__)

__author__ = 'calthorpe'

def post_save_publishing(signal_path, config_entity, user, **kwargs):
    """
        :signal_path - the full module path of the signal that called this
        :param kwargs:
            signal_proportion_lookup - A dictionary of signal names to the proportion complete of the overall post save.
            The signal matching signal_path will be sought in the dictionary
            config_entity - The scope of whatever being post-saved, whether a config_entity or something within it
            dependent_signal_paths - Full module signal paths called in sequentially by this publisher
            crud_type - CrudKey.CREATE|CLONE|UPDATE|SYNC|DELETE
    """
    # TODO config_enity is null for BuiltForm publishing. It should move to kwargs
    api_key = ApiKey.objects.get(user=user).key

    # Pass the arguments to the task and run via celery. Note that kwargs is being treated
    # as a dict here and passed along
    instance_id = kwargs['instance'].id
    instance_class = full_module_path(kwargs['instance'].__class__)
    instance = kwargs.get('instance', resolve_module_attr(instance_class).objects.get(id=instance_id))
    instance_key = kwargs['instance_key'] if kwargs.get('instance_key', None) else instance.key
    logger.info("\tDjango post save instance %s of class %s and id %s" % (instance_key, instance_class, instance_id))

    # If we are not recursing, start celery
    job = start_and_track_task(_post_save_publishing,
                               api_key,
                               config_entity,
                               user,
                               **merge(remove_keys(kwargs, ['instance']),
                                     dict(
                                         # If we are recursing (already in a celery worker, don't start a new celery task
                                         # When we get dependency order figured out, we can do this, but there's probably
                                         # a better way via the Task object or something
                                         current_job=kwargs.get('job', None),
                                         signal_path=signal_path,
                                         instance_class=instance_class,
                                         instance_id=instance_id,
                                         instance_key=instance_key,
                                         crud_type=kwargs.get('crud_type')
                                     )))

    # Send the start event to the client if we aren't recursing.
    if not kwargs.get('recurse', False):
        class_name = instance.__class__.__name__
        event = 'postSavePublisherStarted'
        logger.debug("Sending start message %s to user %s with class_name and %s key %s" % (
            event, user.username, class_name, instance_key)
        )
        send_message_to_client(user.id, dict(
            event=event,
            job_id=str(job.hashid),
            config_entity_id=config_entity and config_entity.id,
            config_entity_class_name=config_entity and config_entity.__class__.__name__,
            # Send the key since the id of new instances might be meaningless to the client
            # If it hasn't updated the record's id yet
            key=instance_key,
            class_name=class_name,
            id=instance_id,
            # Always send 0 for initial
            proportion=0
        ))
    return HttpResponse(job.hashid)


def send_fail_message(config_entity, instance_key, instance_id, instance_class_name, job, publisher_name, signal_proportion_lookup_name,
                user):
    job.status = "Failed"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    readable_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
    job.data = readable_exception
    event = 'postSavePublisherFailed'
    logger.debug("Sending Failed message %s for signal %s to user %s with class_name %s and key %s" % (
    event, signal_proportion_lookup_name, user.username, instance_class_name, instance_key))
    send_message_to_client(user.id, dict(
        event=event,
        config_entity_id=config_entity and config_entity.id,
        config_entity_class_name=config_entity and config_entity.__class__.__name__,
        # Send the key since the id of new instances might be meaningless to the client
        # If it hasn't updated the record's id yet
        key=instance_key,
        class_name=instance_class_name.split('.')[-1], # sometimes full path is passed in
        id=instance_id,
        publisher_name=publisher_name,
        # The client can display a capitalized version of this to describe the progress
        progress_description=humanize(signal_proportion_lookup_name),
        trace=readable_exception)
    )
    return readable_exception


class PostSaveTask(Task):
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Make sure no transactions are outstanding
        # This shouldn't be needed once Django is upgraded
        job, config_entity, user = args
        instance_class_name = kwargs['instance_class']
        instance_id = kwargs['instance_id']
        try:
            instance = resolve_module_attr(instance_class_name).objects.get(id=instance_id)
            instance_key = kwargs.get('instance_key') or instance.key
            instance_class_name = instance.__class__.__name__
        except Exception, e:
            instance = 'Instance id %s no in the database' % instance_id
            instance_key = kwargs.get('instance_key') or 'Unknown'
            instance_class_name = 'Unknown'

        if kwargs.get('created'):
            # Let the instance delete itself on a post save creation error
            instance.handle_post_save_create_error()

        job.ended_on = timezone.now()
        job.save()

        publishing_info = get_publishing_info(**kwargs)
        # Tell the client about the error
        readable_exception = send_fail_message(
            config_entity,
            instance_key,
            instance_id,
            instance_class_name,
            job,
            publishing_info['publisher_name'],
            publishing_info['signal_proportion_lookup_name'],
            user)
        raise Exception(''.join(readable_exception))

    def on_success(self, retval, task_id, args, kwargs):
        job, config_entity, user = args
        job.ended_on = timezone.now()
        job.save()


def get_publishing_info(**kwargs):
    signal_path = kwargs['signal_path']
    signal_proportion_lookup_name = signal_path.split('.')[-1]
    publisher_name = unicode(
        camelize(
            signal_proportion_lookup_name,
            False
        )
    )
    # Lookup the dependent signal paths of the signal. We'll use these to recurse
    dependent_signal_paths = kwargs['dependent_signal_paths'](signal_path)
    proportion = kwargs.get('signal_proportion_lookup', {}).get(signal_proportion_lookup_name, 0)
    return dict(
        publisher_name=publisher_name,
        signal_path=signal_path,
        signal_proportion_lookup_name=signal_proportion_lookup_name,
        proportion=proportion,
        dependent_signal_paths=dependent_signal_paths)


@app.task(base=PostSaveTask)
def _post_save_publishing(job, config_entity, user, **kwargs):
    """
        Runs all configured publishers via the Django signals they depend upon.
        This is done in Celery in order to support long running tasks launched from a client.
        Peer tasks are run in parallel. Dependent tasks are called after the tasks they depend on complete

    :param hash_id: Job hash id
    :param config_entity:
    :param user: The current user or None if no user is in scope
    :return:
    """

    instance_class_name = kwargs['instance_class']
    instance_id = kwargs['instance_id']

    # Get the publisher_name, proportion, and signal_path
    publishing_info = get_publishing_info(**kwargs)

    try:
        # Make sure no transactions are outstanding
        # This shoudln't be needed once Django is upgraded
        transaction.commit()
    except Exception, e:
        pass

    instance = resolve_module_attr(instance_class_name).objects.get(id=instance_id)
    instance_key = kwargs.get('instance_key') or instance.key
    instance_class_name = instance.__class__.__name__

    # Updated the kwargs to include the resolved instance. This will be sent when we recurse on post_save_publishing
    # Also use first=False to indicate recursion so we don't resend the start signal to the client
    updated_kwargs = merge(
        remove_keys(kwargs, ['signal_path', 'instance_class', 'instance_id', 'current_job']),
        dict(instance=instance, recurse=True, current_job=job))

    # TODO causing duplicate pk errors in concurrent mode
    #job.status = 'Started'
    #job.save()

    logger.debug("\tRunning handlers for signal {signal_path} for key {key}".format(
        config_entity=config_entity,
        username=user.username,
        signal_path=publishing_info['signal_path'],
        key=instance_key))

    # Send the signal. The listening publishers will run in sequence
    resolve_module_attr(publishing_info['signal_path']).send(sender=config_entity.__class__ if config_entity else instance.__class__, **updated_kwargs)
    try:
        # Make sure no transactions are outstanding
        # This shouldn't be needed once Django is upgraded
        transaction.commit()
    except Exception, e:
        pass


    event = 'postSavePublisherProportionCompleted'
    logger.debug("Sending message %s for signal complete %s to user %s with class_name %s, key %s, and proportion %s" %
                 (event, publishing_info['signal_proportion_lookup_name'], user.username, instance_class_name, instance_key, publishing_info['proportion']))

    send_message_to_client(user.id, dict(
        event=event,
        job_id=str(job.hashid),
        config_entity_id=config_entity and config_entity.id,
        config_entity_class_name=config_entity and config_entity.__class__.__name__,
        # Send the key since the id of new instances might be meaningless to the client
        # If it hasn't updated the record's id yet
        key=instance_key,
        publisher_name=publishing_info['publisher_name'],
        class_name=instance_class_name,
        id=instance.id,
        # Send the proportion of work that completing this signal signifies--0 to 1
        proportion=publishing_info['proportion'],
        # The client can display a this to describe the progress
        progress_description=humanize(publishing_info['signal_path']),
    ))

    # Find all dependent signals of this one and run each in parallel
    for dependent_signal_path in publishing_info['dependent_signal_paths']:
        post_save_publishing(
            dependent_signal_path,
            config_entity,
            user,
            **updated_kwargs
        )
    job.status = 'Complete'
