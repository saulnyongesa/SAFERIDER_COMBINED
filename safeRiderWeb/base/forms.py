# from django import forms
# from django.db.models import TextField
from django.forms import ModelForm

from base.models import *


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'second_name',
            'last_name',
            'email',
        ]
        # widgets = {
        #     "first_name":  forms.TextInput(attrs={'style': 'text-transform: uppercase;'}),
        #     "second_name":  forms.TextInput(attrs={'style': 'text-transform: uppercase;'}),
        #     "last_name":  forms.TextInput(attrs={'style': 'text-transform: uppercase;'}),
        # }


class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = [
            'stage_name',
            'location'
        ]


class StageAdminForm(ModelForm):
    class Meta:
        model = StageAdmin
        fields = [
            'name',
            'id_number'
        ]


class EmergencyContactsForm(ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [
            'name'
        ]


class StageAddForm(ModelForm):
    class Meta:
        model = Stage
        fields = "__all__"
