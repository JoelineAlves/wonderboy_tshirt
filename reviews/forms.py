from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    """
    A form for submitting product reviews, including a title, text review, and a rating.

    This form allows users to submit feedback about a product, with a title,
    a detailed review, and a rating score between 1 and 5.
    """

    class Meta:
        """
        Defines metadata for the ProductReviewForm.

        Attributes:
            model (Model): Specifies that the form is based on the ProductReview model.
            fields (list): Includes only 'title', 'review', and 'rating' for submission.
            widgets (dict): Customizes field appearances, including placeholders
                            and input constraints for better user experience.
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
        Initializes the form with custom attributes and styling.

        This method dynamically applies CSS classes and placeholders to improve
        the form's usability and appearance.

        Args:
            *args: Positional arguments passed to the parent class.
            **kwargs: Keyword arguments passed to the parent class.
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

        # Remove default field labels to simplify UI
        for field_name in self.fields:
            self.fields[field_name].label = False

    def clean_rating(self):
        """
        Validates the rating field to ensure it is within the allowed range.

        This method is automatically called by Django Forms before saving
        the form data. If the rating is not between 1 and 5, it raises a
        ValidationError.

        Returns:
            int: The cleaned rating value.

        Raises:
            forms.ValidationError: If the rating is not within the valid range.
        """
        rating = self.cleaned_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
