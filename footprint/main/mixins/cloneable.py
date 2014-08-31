from django.db import models

__author__ = 'calthorpe'

class Cloneable(models.Model):
    origin_instance = models.ForeignKey('self', null=True)

    class Meta(object):
        abstract = True
