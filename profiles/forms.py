"""
Forms for managing user profiles.
"""

from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information, including default
    shipping details such as phone number, address, and postcode.
    """

    class Meta:
        model = UserProfile
        exclude = ('user',)  

    def __init__(self, *args, **kwargs):
        """
        Customize form fields by:
        - Adding placeholders for better UX.
        - Setting autofocus on the phone number field.
        - Removing auto-generated labels.
        - Adding consistent CSS classes for styling.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True  

        for field in self.fields:
            if field != 'default_country':  
                placeholder = f"{placeholders[field]} *" if self.fields[field].required else placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False  
