from django import forms

from .models import Expense


class CustomerRecordQueryForm(forms.Form):
  start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                               label="開始日期")
  end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                             label="結束日期")


class ExpenseForm(forms.ModelForm):
  class Meta:
    model = Expense
    fields = ['date', 'item', 'amount', 'payment_method', 'receipt',
              'category', 'remarks']
    widgets = {
      'date': forms.DateInput(
          attrs={'type': 'date', 'class': 'form-control'}),
      'item': forms.TextInput(attrs={'class': 'form-control'}),
      'amount': forms.NumberInput(attrs={'class': 'form-control'}),
      'payment_method': forms.Select(attrs={'class': 'form-control'}),
      'category': forms.Select(attrs={'class': 'form-control'}),
      'remarks': forms.Textarea(attrs={'class': 'form-control'}),
    }


class ExpenseQueryForm(forms.Form):
  year = forms.IntegerField(label='年份', min_value=2000, max_value=2100,
                            widget=forms.NumberInput(
                                attrs={'class': 'form-control'}))
  month = forms.IntegerField(label='月份', min_value=1, max_value=12,
                             widget=forms.NumberInput(
                                 attrs={'class': 'form-control'}))
