from django import forms
from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('name', 'email',)

    def __init__(self, *args, **kwargs):
        """Add placeholders, classes, autofocus, and ARIA attributes."""
        super().__init__(*args, **kwargs)

        # Placeholders
        placeholders = {
            'name': 'Name',
            'email': 'Email',
        }

        # Autofocus and ARIA attributes
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].widget.attrs['aria-label'] = 'Name'
        self.fields['email'].widget.attrs['aria-label'] = 'Email'

        # Placeholder, class, and label adjustments
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0'
            self.fields[field].label = False