from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^save/(?P<path>[\w\/]+)$', 'draft.views.save'),
    url(r'^load/(?P<path>[\w\/]+)$', 'draft.views.load'),
    url(r'^discard/(?P<path>[\w\/]+)$', 'draft.views.discard'),
)
