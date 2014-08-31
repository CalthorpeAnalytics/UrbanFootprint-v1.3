from __future__ import absolute_import
from signal import pause
from fabric.decorators import task
import time

__author__ = 'calthorpe_associates'

import os
from django.conf import settings
from footprint.main.models import Job
from django.utils import timezone
from footprint.celery import app
from boto import ec2, boto
#
# def fp_job(function):
#
#     @app.task  #(name=function.func_name)
#     def tracked_job(job, *args):
#         job.status = 'Started'
#         job.save()
#
#         try:
#             function(job, *args)
#             job.status = 'Complete'
#         #
#         except Exception, e:
#             job.status = "Failed"
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             readable_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
#             job.data = readable_exception
#             send_message_to_client(job.user.id, dict(event=job.type + " failed", trace=readable_exception))
#
#         job.ended_on = timezone.now()
#         job.save()
#
#     return tracked_job


@app.task
def cleanup_export_job(*args, **kwargs):
    jobs_to_clean = Job.objects.filter(type="_export_layer", status="Complete")
    for job in jobs_to_clean:
        if timezone.now() - job.ended_on > settings.DOWNLOAD_FILE_EXPIRY:
            filepath = settings.SENDFILE_ROOT + job.data
            os.remove(filepath)
            job.delete()
        else:
            continue


def connect_ec2():
    from boto.sts import STSConnection
    sts_connection = STSConnection()
    manager = sts_connection.assume_role(role_arn="arn:aws:iam::376704140439:role/manager", role_session_name="ManagerSession")
    region = ec2.get_region("us-west-2")
    connection = ec2.EC2Connection(aws_access_key_id=manager.credentials.access_key, aws_secret_access_key=manager.credentials.secret_key, security_token=manager.credentials.session_token, region=region)
    return connection


def get_instance_by_name(connection, name):
    reservations = connection.get_all_instances(filters={'tag-key': 'Name', 'tag-value': name})
    instances = [r.instances[0] for r in reservations if r.instances[0].tags['Name'] == name]
    if len(instances) > 1:
        raise Exception(name + " returned more than one instance")

    return instances[0]


@app.task
def turn_instance_on(name):
    """turns on an amazon ec2 instance
    :param name: the 'Name' tag of the instance
    :type name: string
    """
    if not name:
        raise Exception("No name was provided")

    connection = connect_ec2()
    instance = get_instance_by_name(connection, name)
    connection.start_instances([instance.id])

    if instance.tags.get('IP', None):
        i = 0
        while i < 10:
            try:
                connection.associate_address(instance.id, instance.tags['IP'])
                i = 10
            except:
                time.sleep(5)
                i += 1
    else:
        print "Instance {name} has no IP assigned to it! Leaving it as randomly assigned"


@app.task
def turn_instance_off(name):
    """turns off an amazon ec2 instance
    :param name: the 'Name' tag of the instance
    :type name: string
    """
    if not name:
        raise Exception("No name was provided")
    connection = connect_ec2()
    instance = get_instance_by_name(connection, name)
    connection.stop_instances([instance.id])


