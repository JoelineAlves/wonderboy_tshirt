"""
Models for managing user profiles.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A model representing a user profile, storing default delivery
    information and order history.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        default_phone_number (CharField): Optional phone number for deliveries.
        default_street_address1 (CharField): Primary street address.
        default_street_address2 (CharField): Secondary street \
        address (optional).
        default_town_or_city (CharField): Town or city for delivery.
        default_county (CharField): County, state, or locality for delivery.
        default_postcode (CharField): Postal or ZIP code.
        default_country (CountryField): Country selection \
        using django-countries.

    Methods:
        __str__(): Returns the username associated with the profile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_county = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_country = CountryField(
        blank_label='Country', null=True, blank=True
    )

    def __str__(self):
        """
        Returns a string representation of the user profile,
        displaying the associated username.
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the user profile when a User instance is saved.

    - If a new user is created, a corresponding UserProfile is also created.
    - If an existing user is updated, their profile is saved to reflect \
    changes.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

