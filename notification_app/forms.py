from django.forms import ModelForm
from django import forms
from .models import *
from django.forms.widgets import DateInput, Select 

class EventForm(forms.ModelForm):
    class Meta:
        model = BroadcastNotification
        fields = ['name', 'broadcast_on', 'end_on', 'cost', 'description']
        widgets = {
            'name': Select(attrs={'class': 'form-control'}),
            'broadcast_on': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_on': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'cost': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add the cost here if applicable...'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add some details here..'}),
        }


    # def __init__(self, *args, **kwargs):
    #     super(EventForm, self).__init__(*args, **kwargs)
        # Customize the 'event' field to use checkboxes
        # self.fields['event'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-input'})
        # self.fields['event'].queryset = FarmEvent.objects.all() 

class FarmEventDetailsForm(forms.ModelForm):
    class Meta:
        model = FarmEventDetails
        fields = ['description']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': '',
        }

