from django.db import models
from django.utils import timezone  # Importando o timezone

class Newsletters(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='newsletter_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True)  # Data de publicação automática
    is_active = models.BooleanField(default=True)  # Campo para indicar se a newsletter está ativa

    def __str__(self):
        return self.title

class SubscribeToNewsletter(models.Model):
    email = models.EmailField(unique=True)
    newsletter = models.ForeignKey(Newsletters, on_delete=models.CASCADE, null=True, blank=True)  # Permite nulo até que existam boletins
    date_subscribed = models.DateTimeField(default=timezone.now)  # Definindo o valor padrão como a data e hora atuais

    def __str__(self):
        return self.email







