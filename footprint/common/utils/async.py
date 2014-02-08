import logging
import re
from django.contrib.auth.models import User
import sys
from tastypie.models import ApiKey
from footprint.main.models import Job

__author__ = 'calthorpe'
logger = logging.getLogger(__name__)

def start_and_track_task(celery_task, api_key, *args, **kwargs):
    user_id = ApiKey.objects.get(key=api_key).user_id

    job = Job.objects.create(
        type=re.split(r'\.', celery_task.name)[-1],
        status="New",
        user=User.objects.get(id=user_id)
    )
    job.save()
    job = Job.objects.get(hashid=job.hashid)

    current_task = celery_task.apply_async(
        args=list((job,) + args),
        kwargs=kwargs,
        soft_time_limit=3600,
        time_limit=3600,
        countdown=1
    )

    if isinstance(current_task.result, Exception):
        # This only works if Celery is set to eager
        logger.error("Celery Task Error: %s",  current_task.result, exc_info=1)
        raise Exception("Celery Task Error: %s. Traceback: %s" % (current_task.result, job.data)), None, sys.exc_info()[2]

    job.task_id = current_task.id
    job.save()

    return job