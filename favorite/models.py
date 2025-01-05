from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # Import the Product model from your products app

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Links to the product

    class Meta:
        unique_together = ('user', 'product')  # Ensures no duplicate product in user's favorites

    def __str__(self):
        return f"{self.user.username} favorited {self.product.name}"


