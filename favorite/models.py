from django.db import models
from django.contrib.auth.models import User
from products.models import Product  

class Favorite(models.Model):
    """
    Model representing a user's favorite products.  

    This model establishes a many-to-many relationship between users and products,  
    allowing users to mark products as favorites. Each user can favorite a product only once.  

    Attributes:  
        user (ForeignKey): A reference to the User who favorited the product.  
        product (ForeignKey): A reference to the favorited Product.  

    Meta:  
        unique_together: Ensures that a user cannot favorite the same product multiple times.  

    Methods:  
        __str__(): Returns a string representation of the favorite, displaying the username  
                   and the name of the favorited product.  
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user.username} favorited {self.product.name}"



