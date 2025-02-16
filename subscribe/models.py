from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    """
    Model representing a newsletter subscriber.

    Attributes:
        name (CharField): The name of the subscriber, limited to \
        100 characters.
        email (EmailField): The unique email address of the subscriber.
        date_subscribed (DateTimeField): The date and time when the \
        subscription was created.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    date_subscribed = models.DateTimeField(
        'Date created', default=timezone.now)

    def __str__(self):
        """
        Returns:
            str: The subscriber's email address as the string \
            representation of the object.
        """
        return self.email


