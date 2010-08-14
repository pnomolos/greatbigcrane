from django.shortcuts import render_to_response
from django.template import RequestContext

from preferences.forms import PreferencesForm
from preferences.models import Preference

def preferences(request):
    form = PreferencesForm(request.POST or None, initial=dict(
        [(p.name, p.value) for p in Preference.objects.all()]))
    if form.is_valid():
        for name, value in form.cleaned_data.iteritems():
            preference, created = Preference.objects.get_or_create(name=name)
            preference.value = value
            preference.save()

    return render_to_response("preferences/preferences.html", RequestContext(
        request, {'form': form}))
