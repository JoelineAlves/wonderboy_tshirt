from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from math import floor


class ProductReview(models.Model):
    """
    Model representing a product review.

    This model stores customer reviews for a specific product, including
    the review title, description, rating, and the date the review was created.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_reviews_from_reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the review.

        Returns:
            str: The title of the review.
        """
        return self.title

    @classmethod
    def get_average_rating(cls, product):
        """
        Calculate the average rating for a given product.

        Args:
            product (Product): The product for which the average \
            rating is calculated.

        Returns:
            float: The average rating for the product, rounded to \
            one decimal place,
                   or 0 if no reviews exist.
        """
        reviews = cls.objects.filter(product=product)
        if reviews.exists():
            total_rating = reviews.aggregate(
                models.Sum('rating')
            )['rating__sum']
            count = reviews.count()
            return round(total_rating / count, 1)
        return 0

    def stars(self):
        """
        Calculate the number of full stars based on the rating.

        This method is typically used in templates to display star ratings.

        Returns:
            range: A range object representing the number of full stars.
        """
        return range(floor(self.rating))

    def half_star(self):
        """
        Determine if the rating includes a half-star.

        This method is used in templates to conditionally render a \
        half-star icon.

        Returns:
            bool: True if the rating includes a half-star, False otherwise.
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




