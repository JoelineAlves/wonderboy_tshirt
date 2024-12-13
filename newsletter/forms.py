from django import forms
from django import forms
from .models import Newsletters

class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletters
        fields = [
            'title', 
            'content', 
            'date_published',
            'image',
            'image_url'
        ]
        widgets = {
            'date_published': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {  
            'title': 'Title',
            'content': 'Content',
            'date_published': 'Date Published',
            'image': 'Image',
            'image_url': 'Image URL'
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

        for field in self.fields:
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = ' '.join(classes)
