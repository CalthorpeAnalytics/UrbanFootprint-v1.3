from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from models import Draft
from django.contrib import messages

@require_POST
def save(request, path):
    draft, created = Draft.objects.get_or_create(path=path)
    draft.serialized_data = request.POST.urlencode()
    draft.save()
    messages.add_message(request, messages.INFO, _(u'Draft saved'))
    return HttpResponseRedirect('/%s' % path)
    
@require_GET
def load(request, path):
    try:
        draft = Draft.objects.get(path=path)
        return HttpResponse(draft.serialized_data)
    except Draft.DoesNotExist:
        return HttpResponse('')

@require_POST
def discard(request, path):
    try:
        Draft.objects.get(path=path).delete()
        messages.add_message(request, messages.INFO, _(u'Draft deleted'))
    except Draft.DoesNotExist:
        messages.add_message(request, messages.ERROR, _(u'There was no draft corresponding to this document.'))
    
    return HttpResponseRedirect('/%s' % path)