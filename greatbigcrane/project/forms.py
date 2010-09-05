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

from project.models import Project

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project

    def clean_base_directory(self):
        value = self.cleaned_data['base_directory']
        return os.path.expanduser(value).strip()

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_git_repo(self):
        return self.cleaned_data['git_repo'].strip()

    def clean_description(self):
        return self.cleaned_data['description'].strip()
