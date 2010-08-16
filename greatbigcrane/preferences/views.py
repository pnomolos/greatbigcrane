"""
Copyright 2010 Jason Chu, Dusty Phillips, and Phil Schalm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.shortcuts import render_to_response
from django.template import RequestContext

from preferences.forms import PreferencesForm
from preferences.models import Preference

def preferences(request):
    """Render a simple preference editing form."""
    form = PreferencesForm(request.POST or None, initial=dict(
        [(p.name, p.value) for p in Preference.objects.all()]))
    if form.is_valid():
        for name, value in form.cleaned_data.iteritems():
            preference, created = Preference.objects.get_or_create(name=name)
            preference.value = value
            preference.save()

    return render_to_response("preferences/preferences.html", RequestContext(
        request, {'form': form}))
