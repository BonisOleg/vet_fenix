from django import forms

from clinic.models import ContactMessage

REQUIRED_FIELD_MSG = 'Заповніть це поле.'


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'field-input', 'placeholder': 'Ваше імʼя'},
            ),
            'phone': forms.TelInput(
                attrs={'class': 'field-input', 'placeholder': '+380...'},
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'field-input',
                    'placeholder': 'Ваше питання або коментар',
                    'rows': 3,
                },
            ),
        }
        error_messages = {
            'name': {'required': REQUIRED_FIELD_MSG},
            'phone': {'required': REQUIRED_FIELD_MSG},
            'message': {'required': REQUIRED_FIELD_MSG},
        }

    def clean_phone(self) -> str:
        phone = self.cleaned_data['phone'].strip()
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Введіть коректний номер телефону.')
        return phone
