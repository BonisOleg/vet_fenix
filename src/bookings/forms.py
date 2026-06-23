from datetime import date, timedelta

from django import forms
from django.conf import settings

from bookings.models import AppointmentRequest, CallbackLead
from clinic.forms import REQUIRED_FIELD_MSG
from clinic.models import Doctor, Service


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = [
            'service',
            'doctor',
            'owner_name',
            'phone',
            'pet_name',
            'pet_type',
            'preferred_date',
            'preferred_time',
            'comment',
        ]
        widgets = {
            'service': forms.Select(attrs={'class': 'field-select'}),
            'doctor': forms.Select(attrs={'class': 'field-select'}),
            'owner_name': forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Ваше імʼя'}),
            'phone': forms.TelInput(attrs={'class': 'field-input', 'placeholder': '+380...'}),
            'pet_name': forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Кличка'}),
            'pet_type': forms.Select(attrs={'class': 'field-select'}),
            'preferred_date': forms.DateInput(attrs={'class': 'field-input', 'type': 'date'}),
            'preferred_time': forms.Select(attrs={'class': 'field-select'}),
            'comment': forms.Textarea(
                attrs={'class': 'field-input', 'rows': 3, 'placeholder': 'Коментар (необовʼязково)'},
            ),
        }
        error_messages = {
            'service': {'required': REQUIRED_FIELD_MSG},
            'owner_name': {'required': REQUIRED_FIELD_MSG},
            'phone': {'required': REQUIRED_FIELD_MSG},
            'pet_type': {'required': REQUIRED_FIELD_MSG},
            'preferred_date': {'required': REQUIRED_FIELD_MSG},
            'preferred_time': {'required': REQUIRED_FIELD_MSG},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = 'Оберіть послугу'
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['doctor'].required = False
        self.fields['doctor'].empty_label = 'Будь-який лікар'
        self.fields['pet_type'].choices = [('', 'Оберіть тварину'), *settings.PET_TYPE_CHOICES]
        self.fields['preferred_time'].choices = [('', 'Оберіть час'), *[
            (t, t) for t in settings.BOOKING_TIME_SLOTS
        ]]
        self.fields['preferred_date'].widget.attrs['min'] = date.today().isoformat()
        self.fields['preferred_date'].widget.attrs['max'] = (
            date.today() + timedelta(days=13)
        ).isoformat()
        if not self.is_bound and 'preferred_date' not in self.initial:
            self.initial.setdefault('preferred_date', date.today())

    def clean_phone(self):
        return _clean_phone(self.cleaned_data['phone'])


class CallbackLeadForm(forms.ModelForm):
    class Meta:
        model = CallbackLead
        fields = ['name', 'phone', 'service', 'comment']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'field-input', 'placeholder': "Ваше імʼя *"},
            ),
            'phone': forms.TelInput(
                attrs={'class': 'field-input', 'placeholder': 'Номер телефону *'},
            ),
            'service': forms.Select(attrs={'class': 'field-select'}),
            'comment': forms.Textarea(
                attrs={'class': 'field-input', 'rows': 3, 'placeholder': 'Коментар'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].required = False
        self.fields['service'].empty_label = 'Оберіть послугу'
        self.fields['name'].required = True
        self.fields['phone'].required = True

    def clean_phone(self):
        return _clean_phone(self.cleaned_data['phone'])


def _clean_phone(phone: str) -> str:
    phone = phone.strip()
    digits = ''.join(c for c in phone if c.isdigit())
    if len(digits) < 10:
        raise forms.ValidationError('Введіть коректний номер телефону.')
    return phone
