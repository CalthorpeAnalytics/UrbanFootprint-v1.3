from __future__ import absolute_import

__author__ = 'calthorpe_associates'

import os

from django.utils import timezone

from django.conf import settings
from footprint.main.models import Job
from footprint.celery import app

from footprint.main.publishing.data_export_publishing import _export_layer
from footprint.main.publishing.config_entity_publishing import _post_save_publishing

import sys
import traceback
from django.utils import timezone
from footprint.celery import app
from footprint.common.utils.websockets import send_message_to_client

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
def cleanup_export_job():
    jobs_to_clean = Job.objects.filter(type="_export_layer", status="Complete")
    for job in jobs_to_clean:
        if timezone.now() - job.ended_on > settings.DOWNLOAD_FILE_EXPIRY:
            filepath = settings.SENDFILE_ROOT + job.data
            os.remove(filepath)
            job.delete()
        else:
            continue