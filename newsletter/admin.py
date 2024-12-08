from django.contrib import admin
from .models import Newsletters, SubscribeToNewsletter

class NewslettersAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'is_active')  # Show title, publication date, and active status
    list_filter = ('is_active',)  # Filter by active status
    search_fields = ('title',)  # Allow search by title

class SubscribeToNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'newsletter', 'date_subscribed')  # Show email, newsletter, and subscription date
    list_filter = ('newsletter',)  # Filter by newsletter
    search_fields = ('email',)  # Allow search by email

admin.site.register(Newsletters, NewslettersAdmin)
admin.site.register(SubscribeToNewsletter, SubscribeToNewsletterAdmin)




