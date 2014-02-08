from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.filter
def jsonify(obj):
    if isinstance(obj, QuerySet):
        return mark_safe(serialize('json', obj))
    return mark_safe(simplejson.dumps(obj, cls=DjangoJSONEncoder))
