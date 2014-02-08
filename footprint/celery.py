from __future__ import absolute_import
__author__ = 'calthorpe_associates'

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'footprint.settings')

app = Celery('footprint',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                include=['footprint.main.publishing.config_entity_publishing',
                         'footprint.main.publishing.data_export_publishing',
                         'footprint.main.publishing.data_import_publishing',
                         'footprint.main.models.analysis_module'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# app.conf.update(
#     CELERYD_USER="calthorpe",
#     CELERYD_GROUP="www-data"
# )
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))