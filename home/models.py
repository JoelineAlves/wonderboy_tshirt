# home/models.py

from django.db import models
from django.contrib.auth.models import User

class SubscribeToNewsletter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

