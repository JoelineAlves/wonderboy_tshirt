from django import forms
from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    """
    Form for subscribing users by collecting their name and email.

    Attributes:
        Meta:
            model (Subscriber): Specifies that the form is based on the \
            Subscriber model.
            fields (tuple): Specifies the fields to be included in the \
            form ('name', 'email').
    """
    class Meta:
        model = Subscriber
        fields = ('name', 'email',)

    def __init__(self, *args, **kwargs):
        """Add placeholders, classes, autofocus, and ARIA attributes."""
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': 'Name',
            'email': 'Email',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].widget.attrs['aria-label'] = 'Name'
        self.fields['email'].widget.attrs['aria-label'] = 'Email'

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0'
            self.fields[field].label = False
