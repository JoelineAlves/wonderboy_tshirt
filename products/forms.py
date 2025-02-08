"""
Forms for managing products in the application.
"""

from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


# Add product form
class ProductForm(forms.ModelForm):
    """
    Form for adding or updating a product.
    """

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with category choices and apply custom styles to fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
