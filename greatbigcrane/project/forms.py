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

from django import forms

from project.models import Project
from buildout_manage.buildout_config import buildout_write

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

class DjangoRecipeForm(forms.Form):
    name = forms.CharField(initial="django")
    settings = forms.CharField()
    version = forms.ChoiceField(choices=[
        ("trunk", "trunk"),
        ("1.2", "1.2"),
        ("1.1.2", "1.1.2"),
        ("1.1", "1.1"),
        ("1.0.4", "1.04"),
        ("0.96", "0.96"),
        ])
    eggs = forms.CharField(required=False)
    project = forms.CharField(required=False)
    extra_paths = forms.CharField(required=False)
    fcgi = forms.BooleanField(required=False)
    wsgi = forms.BooleanField(required=False)

    def save(self, project, buildout):
        name = self.cleaned_data['name']
        for key in self.fields:
            if key == "name": continue
            buildout[name][key] = self.cleaned_data[key]
        buildout_write(project.buildout_filename(), buildout)


recipe_form_map = {
        'djangorecipe': DjangoRecipeForm
        }
