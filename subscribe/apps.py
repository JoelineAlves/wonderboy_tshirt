from django.apps import AppConfig

class SubscribeConfig(AppConfig):
    """
    App configuration for the 'subscribe' app.

    Attributes:
        default_auto_field (str): Defines the default primary key field type.
        name (str): Specifies the name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscribe'

