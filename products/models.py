from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """ Category Model """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """ Products Model """

    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    """
    Product Review Model

    This model represents reviews submitted by users for a specific product.
    Each review includes a title, detailed feedback, a rating, and the date
    it was created.

    Attributes:
        product (ForeignKey): The product being reviewed.
        user (ForeignKey): The user who submitted the review.
        title (CharField): The title of the review.
        review (TextField): The detailed content of the review.
        rating (PositiveIntegerField): A rating given to the product (1-5).
        date (DateTimeField): The date and time the review was submitted.

    Meta:
        ordering: Orders reviews by newest first.

    Methods:
        __str__(): Returns a string representation of the review,
                   showing the product name and the user who submitted it.
    """

    product = models.ForeignKey(
        Product,
        related_name="product_reviews_from_products",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

