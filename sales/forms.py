# forms.py
from django import forms
from .models import SaleSubmission

class SaleSubmissionForm(forms.ModelForm):
    class Meta:
        model = SaleSubmission
        fields = ['items_sold', 'notes']
        widgets = {
            'items_sold': forms.NumberInput(attrs={
                'class': 'form-field mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm p-4',
                'placeholder': 'Enter number of items sold',
                'min': '1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'rows': 3,
                'placeholder': 'Any additional notes about the sales'
            })
        }