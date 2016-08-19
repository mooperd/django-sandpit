from django import forms

class VpcForm(forms.Form):
    name = forms.CharField()
    subnet = forms.CharField()
