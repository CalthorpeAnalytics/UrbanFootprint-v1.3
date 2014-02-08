import json
import datetime
import os
from django.contrib.auth.models import User
from django.utils import timezone
from fabric.decorators import task
from settings import SENDFILE_ROOT, DOWNLOAD_FILE_EXPIRY

__author__ = 'calthorpe'

from django.db import models
import uuid

class Job(models.Model):
    hashid = models.CharField(max_length=36, unique=True)
    task_id = models.CharField(max_length=36)
    user = models.ForeignKey(User, related_name='jobs')
    type = models.CharField(max_length=32)
    status = models.TextField(blank=True)  # JSON
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True)
    data = models.CharField(max_length=10000, null=True)

    def __unicode__(self):
        return u'Job %s' % self.hashid

    def save(self, *args, **kwargs):
        if not self.hashid:
            self.hashid = uuid.uuid4()
        super(Job, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']
        app_label = 'footprint'

