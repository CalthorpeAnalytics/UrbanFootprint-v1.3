import logging
import re
from django.contrib.auth.models import User
from django.db import transaction
from tastypie.models import ApiKey
from footprint.main.models.tasks.async_job import Job

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
    try:
        # Make sure no transactions are outstanding
        # This shouldn't be needed once Django is upgraded
        transaction.commit()
    except Exception, e:
        pass

    current_task = celery_task.apply_async(
        args=list((job,) + args),
        kwargs=kwargs,
        soft_time_limit=3600,
        time_limit=3600,
        countdown=1
    )

    job = Job.objects.get(hashid=job.hashid)
    job.task_id = current_task.id
    job.save()

    return job