from django import forms

class StartAppForm(forms.Form):
    app_name = forms.CharField()
