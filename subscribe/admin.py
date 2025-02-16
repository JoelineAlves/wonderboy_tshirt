from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subscriber model.

    Displays the following fields in the admin list view:
    - email (str): The subscriber's email address.
    - name (str): The subscriber's name.
    - date_subscribed (datetime): The date and time the user subscribed.
    """
    list_display = ('email', 'name', 'date_subscribed')


admin.site.register(Subscriber, SubscriberAdmin)


