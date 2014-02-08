from django.db import models

__author__ = 'calthorpe'

class PostSaveStatus(models.Model):
    """
        A status to help track asynchronous post-save publishers
    """
    post_save_status = models.IntegerField(default=False)

    class Meta(object):
        abstract = True

PostSaveStatus.STATUS_READY_NEW = 2
PostSaveStatus.STATUS_READY_COMPLETE = 3
PostSaveStatus.STATUS_BUSY = 4
PostSaveStatus.STATUS_ERROR = 8
