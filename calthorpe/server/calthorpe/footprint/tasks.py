import os
from celery.task import task
from settings import DOWNLOAD_FILE_EXPIRY, SENDFILE_ROOT

__author__ = 'calthorpe'

from footprint.models.tasks.async_job import Job
from footprint.publishing.data_export import _export_layer
from footprint.publishing.config_entity_creation import _post_create_config_entity

from time import sleep, timezone
import boto.ec2


@task(name='cleanup_export_job')
def cleanup_export_job():
    jobs_to_clean = Job.objects.filter(type="export_layer", status="Complete")
    for job in jobs_to_clean:
        if timezone.now() - job.ended_on > DOWNLOAD_FILE_EXPIRY:
            filepath = SENDFILE_ROOT + job.data
            os.remove(filepath)
            job.data = '[deleted]'
            job.status = 'Cleaned'
            job.save()
        else:
            continue

def get_instance(instance_name):
    connection = boto.ec2.connect_to_region('us-west-2')
    instances = [reservation.instances[0] for reservation in connection.get_all_instances()
                if reservation.instances[0].tags['Name'] == instance_name]
    if not instances:
        print "There are no instances with that name, check your spelling."
        return

    return instances[0]

@task
def turn_instance_off(instance_name):
    instance = get_instance(instance_name)
    instance.stop()

@task
def turn_instance_on(instance_name):
    instance = get_instance(instance_name)
    instance.start()

@task
def change_instance_type(instance_name="SACOG UF", type="t1.micro"):
    """
    Alters the instance type of an Amazon EC2 instance.
    :param type:
    :return:
    """

    # step 0 : connect to the amazon ec2 management console and get the instance by its name tag
    instance = get_instance(instance_name)

    if instance.instance_type == type:
        print "Instance {instance} is already {type}".format(instance=instance.tags['Name'], type=type)
        return

    print "Scaling instance {instance} from {current} to {type}".format(instance=instance.tags['Name'], current=instance.instance_type, type=type)
    # step 1 : shut down the instance
    print "Stopping instance."
    instance.stop()
    print "Waiting for instance to stop..."
    while instance.update() == 'stopping':
        sleep(10)
        print "\tstill waiting..."

    # step 2 : change the instance type
    print "Changing instance type to {type}".format(type=type)
    instance.modify_attribute('instanceType', type)

    # step 3 : start the instance
    print "Starting instance."
    instance.update()
    instance.start()
    print "Waiting for instance to start..."
    while instance.update() == 'pending':
        sleep(10)
        print "\tstill waiting..."

    # step 4 : attach the instance's IP to the instance
    connection = boto.ec2.connect_to_region('us-west-2')

    IP = [ip for ip in connection.get_all_addresses() if ip.public_ip == instance.tags['IP']][0]
    IP.associate(instance.id)
    print "connecting {IP} to {instance}... waiting for it to associate".format(IP=IP, instance=instance.tags['Name'])
    sleep(30)

    assert instance.instance_type == type, "Unable to change instance type -- please go to the Amazon console to investigate"

