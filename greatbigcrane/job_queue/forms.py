from django import forms

class StartAppForm(forms.Form):
    "Simple form to prompt for the appname when running django startapp."
    app_name = forms.CharField()
