from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    """
    A form for submitting product reviews, including a text review and a rating.
    """

    class Meta:
        """
        Meta options for the ProductReviewForm.
        Specifies the model and fields to include in the form.
        """
        model = ProductReview
        fields = ['title', 'review', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'review': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.1}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom attributes and placeholders for the fields.
        """
        super().__init__(*args, **kwargs)

        common_classes = (
            'bg-slate-600 bd-radius-1 transition-fast shadow-focus-1 '
            'sh-sky-300 bd-width-0 width-100 pad-inline-1 ft-serif'
        )

        self.fields['title'].widget.attrs.update({
            'placeholder': 'Title...',
            'class': common_classes,
        })
        self.fields['review'].widget.attrs.update({
            'placeholder': 'Write your review here...',
            'class': common_classes,
        })
        self.fields['rating'].widget.attrs.update({
            'placeholder': 'Rating (1-5)',
            'class': common_classes,
        })

        for field_name in self.fields:
            self.fields[field_name].label = False

    def clean_rating(self):
        """
        Validate the rating field to ensure it is between 1 and 5.
        """
        rating = self.cleaned_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
