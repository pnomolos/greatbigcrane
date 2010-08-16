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
import os.path
from django import forms
from preferences.models import Preference

class PreferencesForm(forms.Form):
    '''Dynamic form for editing key value preferences stored
    in the preferences model of the database.'''
    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)
        for preference in Preference.objects.all():
            self.fields[preference.name] = forms.CharField(help_text=preference.help_text,
                    required=False)

    def clean_projects_directory(self):
        '''Ensure the projects_directory preference has a trailing slash'''
        if not self.cleaned_data['projects_directory'].endswith(os.path.sep):
            self.cleaned_data['projects_directory'] += os.path.sep
        return self.cleaned_data['projects_directory']
