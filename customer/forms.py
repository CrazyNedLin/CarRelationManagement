from django import forms
from django.forms import inlineformset_factory

from .models import Customer, Vehicle, CustomerRecord


class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['name', 'phone', 'address']


VehicleFormSet = inlineformset_factory(Customer, Vehicle, fields=(
  'brand', 'model', 'plate_number'), extra=1, can_delete=True)


class CustomerRecordForm(forms.ModelForm):
  class Meta:
    model = CustomerRecord
    fields = ['date', 'vehicle', 'service_content', 'amount']
    widgets = {
      'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
      'vehicle': forms.Select(attrs={'class': 'form-control'}),
      'service_content': forms.Textarea(attrs={'class': 'form-control'}),
      'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    }
