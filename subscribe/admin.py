from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ('email', 'name', 'date_subscribed')


# Register the Subscriber model with the custom admin configuration
admin.site.register(Subscriber, SubscriberAdmin)
