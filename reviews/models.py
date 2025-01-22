from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from math import floor

class ProductReview(models.Model):
    """
    Modelo representando uma avaliação de produto.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews_from_reviews')  # Alterado o related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)  
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_average_rating(cls, product):
        """
        Calculate the average rating for a product.

        Args:
            product (Product): The product for which to calculate the average rating.

        Returns:
            float: The average rating for the product, or 0 if no reviews exist.
        """
        reviews = cls.objects.filter(product=product)
        if reviews.exists():
            total_rating = reviews.aggregate(models.Sum('rating'))['rating__sum']
            count = reviews.count()
            average_rating = total_rating / count
            return average_rating
        return 0

    def stars(self):
        """
        Calculate the number of full stars for the rating.

        Returns:
            range: A range object to loop through full stars in the template.
        """
        return range(floor(self.rating))

    def half_star(self):
        """
        Determine if there is a half star in the rating.

        Returns:
            bool: True if a half star exists, False otherwise.
        """
        return self.rating % 1 >= 0.5

    @property
    def username(self):
        """
        Retrieve the username of the user who submitted the review.

        Returns:
            str: The username of the associated user.
        """
        return self.user.username


