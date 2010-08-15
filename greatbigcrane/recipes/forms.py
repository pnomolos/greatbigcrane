import re
from django import forms

from project.widgets import LineEditorWidget, LineEditorChoiceWidget
from buildout_manage.parser import buildout_write
from buildout_manage import recipes

class DjangoRecipeForm(forms.Form):
    name = forms.CharField(initial="django")
    settings = forms.CharField(initial="development")
    version = forms.ChoiceField(choices=[
        ("trunk", "trunk"),
        ("1.2.1", "1.2.1"),
        ("1.2", "1.2"),
        ("1.1.2", "1.1.2"),
        ("1.1", "1.1"),
        ("1.0.4", "1.04"),
        ("0.96", "0.96"),
        ])
    eggs = forms.CharField(required=False,widget=LineEditorWidget)
    project = forms.CharField(required=False)
    extra_paths = forms.CharField(required=False,widget=LineEditorWidget)
    fcgi = forms.BooleanField(required=False)
    wsgi = forms.BooleanField(required=False)

    def __init__(self, project, *args, **kwargs):
        super(DjangoRecipeForm, self).__init__(*args, **kwargs)
        self.project = project
        safe_name = re.sub(r'[^A-Za-z0-9_]', '', project.name).lower()
        self.fields['project'].initial = safe_name
        self.fields['eggs'].widget = LineEditorChoiceWidget(choices=[("a", "a"), ("b", "b")])

    def save(self, buildout):
        name = self.cleaned_data['name']
        dr = recipes['djangorecipe'](buildout, name)
        for key in self.fields:
            if key == "name": continue

            value = self.cleaned_data[key]
            if not isinstance(value, bool) and '\r\n' in value:
                value = value.split('\r\n')
            if value:
                setattr(dr, key, value)
            else:
                delattr(dr, key)
        buildout_write(self.project.buildout_filename(), buildout)

class EggRecipeForm(forms.Form):
    name = forms.CharField(initial="eggs")
    eggs = forms.CharField(required=False,widget=LineEditorWidget)
    find_links = forms.CharField(required=False,widget=LineEditorWidget)
    interpreter = forms.CharField(required=False)
    index = forms.CharField(required=False)
    python = forms.CharField(required=False)
    extra_paths = forms.CharField(required=False,widget=LineEditorWidget)
    relative_paths = forms.BooleanField(required=False)
    dependent_scripts = forms.BooleanField(required=False)

    def __init__(self, project, *args, **kwargs):
        super(EggRecipeForm, self).__init__(*args, **kwargs)
        self.project = project


    def save(self, buildout):
        name = self.cleaned_data['name']
        dr = recipes['zc.recipe.egg'](buildout, name)
        for key in self.fields:
            if key == "name": continue

            value = self.cleaned_data[key]
            if not isinstance(value, bool) and '\r\n' in value:
                value = value.split('\r\n')
            if value:
                setattr(dr, key, value)
            else:
                delattr(dr, key)
        buildout_write(self.project.buildout_filename(), buildout)

class GitRecipeForm(forms.Form):
    name = forms.CharField(initial="git")
    repository = forms.CharField(required=True)
    rev = forms.CharField(required=False)
    branch = forms.CharField(required=False)
    paths = forms.CharField(required=False,widget=LineEditorWidget)
    cache_name = forms.CharField(required=False)
    as_egg = forms.BooleanField(required=False)
    newest = forms.BooleanField(required=False)

    def __init__(self, project, *args, **kwargs):
        super(GitRecipeForm, self).__init__(*args, **kwargs)
        self.project = project


    def save(self, buildout):
        name = self.cleaned_data['name']
        dr = recipes['zerokspot.recipe.git'](buildout, name)
        for key in self.fields:
            if key == "name": continue

            value = self.cleaned_data[key]
            if not isinstance(value, bool) and '\r\n' in value:
                value = value.split('\r\n')
            if value:
                setattr(dr, key, value)
            else:
                delattr(dr, key)
        buildout_write(self.project.buildout_filename(), buildout)

class MercurialRecipeForm(forms.Form):
    name = forms.CharField(initial="mercurial")
    repository = forms.CharField(required=True)
    location = forms.CharField(required=False)
    newest = forms.BooleanField(required=False)

    def __init__(self, project, *args, **kwargs):
        super(MercurialRecipeForm, self).__init__(*args, **kwargs)
        self.project = project


    def save(self, buildout):
        name = self.cleaned_data['name']
        dr = recipes['mercurialrecipe'](buildout, name)
        for key in self.fields:
            if key == "name": continue

            value = self.cleaned_data[key]
            if not isinstance(value, bool) and '\r\n' in value:
                value = value.split('\r\n')
            if value:
                setattr(dr, key, value)
            else:
                delattr(dr, key)
        buildout_write(self.project.buildout_filename(), buildout)


recipe_form_map = {
        'djangorecipe': DjangoRecipeForm,
        'zc.recipe.egg': EggRecipeForm,
        'zerokspot.recipe.git': GitRecipeForm,
        'mercurialrecipe': MercurialRecipeForm,
        }
