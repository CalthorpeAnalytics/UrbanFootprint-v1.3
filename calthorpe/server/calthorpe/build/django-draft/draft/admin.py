from django.contrib import admin
from django import forms
from django.conf import settings

class DraftAdmin(admin.ModelAdmin):
    """
    Add draft.js file
    """
    def _media(self):
        from django.conf import settings

        js = ['js/core.js', 'js/admin/RelatedObjectLookups.js',
              'js/jquery.min.js', 'js/jquery.init.js']
        if self.actions is not None:
            js.extend(['js/actions.min.js'])
        if self.prepopulated_fields:
            js.append('js/urlify.js')
            js.append('js/prepopulate.min.js')
        if self.opts.get_ordered_objects():
            js.extend(['js/getElementsBySelector.js', 'js/dom-drag.js' , 'js/admin/ordering.js'])

        js = ['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js]
        js.append('%sdraft/js/draft.js' % (settings.STATIC_URL,))
        return forms.Media(js=js)
    media = property(_media)        