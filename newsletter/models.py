from django.db import models
from django.contrib.auth.models import User


class Newsletters(models.Model):
    # A class for storing the newsletters created by the admin.
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    # The image field is used to store the image of the newsletter. upload to media folder
    image = models.ImageField(upload_to='newsletter/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class SubscribeToNewsletter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email if self.user else (self.email or "No email")








