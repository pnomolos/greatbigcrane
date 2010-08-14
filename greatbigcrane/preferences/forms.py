from django import forms
from preferences.models import Preference

class PreferencesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)
        for preference in Preference.objects.all():
            self.fields[preference.name] = forms.CharField()
