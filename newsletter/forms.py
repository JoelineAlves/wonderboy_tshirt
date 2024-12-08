from django import forms
from .models import SubscribeToNewsletter

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = SubscribeToNewsletter
        fields = ['newsletter', 'email']  # Fields for choosing the newsletter and the email address

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define placeholders and CSS classes for fields
        placeholders = {  
            'email': 'Enter your email',
        }

        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'transition-fast',
            'shadow-focus-1',
            'sh-sky-300',
            'bd-width-0',
            'width-100',
            'pad-inline-1'
        ]

        # Apply the placeholders and classes to the fields
        for field in self.fields:
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = ' '.join(classes)

