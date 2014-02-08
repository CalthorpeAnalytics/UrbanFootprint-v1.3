from django.db import models

__author__ = 'calthorpe'

class Deletable(models.Model):
    deleted = models.BooleanField(default=False)

    def handle_post_save_creation_error(self):
        """
            All deletable instances handle post_save creation process errors by marking themselves as deleted.
        """

        self.deleted = True
        self.save()

    class Meta(object):
        abstract = True
