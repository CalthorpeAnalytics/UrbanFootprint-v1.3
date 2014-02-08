from django import template
from django.conf import settings as django_settings
register = template.Library()

@register.simple_tag(takes_context=True)
def settings(context):
    context['settings'] = django_settings
    return ''