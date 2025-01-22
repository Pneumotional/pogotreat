from django import forms
from .models import VendorApplication, VendorProfile

class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        exclude = ['is_approved']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-field mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'placeholder': 'Enter your full name'
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'form-field mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'placeholder': 'Enter your business name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-field mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'placeholder': 'you@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-field mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'placeholder': 'Enter your phone number'
            }),
            'payment_frequency': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
                'rows': 4,
                'placeholder': 'Your Univeristy and your residential or hostel Adress'
            }),
        }

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        exclude = ['user', 'is_approved', 'commission_rate']
        widgets = {
            'payment_frequency': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm',
            })
        }

