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

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

class DjangoRecipeForm(forms.Form):
    settings = forms.CharField()
    version = forms.ChoiceField(choices=[
        ("trunk", "trunk"),
        ("1.2", "1.2"),
        ("1.1.2", "1.1.2"),
        ("1.1", "1.1"),
        ("1.0.4", "1.04"),
        ("0.96", "0.96"),
        ])
    eggs = forms.CharField()
    project = forms.CharField()
    extra_paths = forms.CharField()
    fcgi = forms.BooleanField()
    wsgi = forms.BooleanField()

recipe_form_map = {
        'djangorecipe': DjangoRecipeForm
        }
