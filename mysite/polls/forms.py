from django import forms

from models import Vpc, Subnet, Instance


class VpcForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'cidr']
        model = Vpc


class SubnetForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'cidr', 'availability_zone']
        model = Subnet


class InstanceForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['name', 'type']
