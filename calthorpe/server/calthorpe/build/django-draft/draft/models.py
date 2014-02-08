from django.utils.translation import ugettext_lazy as _
from django.db import models
class Draft(models.Model):
    """Draft model serializing a form related to an admin url"""
    
    path = models.CharField(_(u'Path'), blank=True, max_length=255, unique=True)
    serialized_data = models.TextField(_(u'Path'), help_text="The serialized form")
    
    class Meta:
        verbose_name_plural = _(u'Drafts')

    def __unicode__(self):
        return u"Draft %s" % (self.path,)
    