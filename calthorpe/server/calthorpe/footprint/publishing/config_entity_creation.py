# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
import traceback
from celery.task import task
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
import sys
from common.utils.websockets import send_message_to_client
from footprint.models import Job
from footprint.models.signals import post_post_save_config_entity


def post_create_config_entity(config_entity, **kwargs):
    # TODO The default user should be the admin
    user = config_entity.creator if config_entity.creator else User.objects.all()[0]
    job = Job.objects.create(
        type="post_create_config_entity",
        status="New",
        user=user
    )
    job.save()

    task = _post_create_config_entity.apply_async(
         args=[job.hashid, config_entity, user],
         soft_time_limit=3600,
         time_limit=3600,
         countdown=1
    )

    job = Job.objects.get(hashid=job.hashid)
    job.task_id = task.id
    job.save()

    return HttpResponse(job.hashid)

@task
def _post_create_config_entity(hash_id, config_entity, user):
    """
        Runs all post_post_save_config_entity listeners. This is done in Celery in order to support long running tasks
        launched from a client, and to potentially run listeners in parallel some day

    :param hash_id: Job hash id
    :param config_entity:
    :param user: The current user or None if no user is in scope
    :return:
    """
    job = Job.objects.get(hashid=hash_id)
    job.status = "Creating"
    job.save()
    try:
        post_post_save_config_entity.send(sender=config_entity.__class__, instance=config_entity)

        job.status = "Complete"
        job.save()

        send_message_to_client(user.id,
                               dict(event='config_entity_creation_complete',
                                    job_id=job.hashid,
                                    config_entity_id=config_entity.id)
        )

    except Exception, E:
        job.status = "Failed"
        job.data = str(E)
        job.save()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        send_message_to_client(user.id,
                               dict(event='config_entity_creation_failed',
                                    config_entity_id=config_entity.id,
                                    trace=traceback.format_exception(exc_type, exc_value, exc_traceback))
        )

    job.ended_on = timezone.now()
    job.save()
