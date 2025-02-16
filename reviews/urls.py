from django.urls import path
from .views import all_reviews, add_review, edit_review, delete_review

urlpatterns = [
    path('all_reviews/<product_id>/', all_reviews, name='all_reviews'),
    path('add_review/<product_id>/', add_review, name='add_review'),
    path('edit_review/<review_id>/', edit_review, name='edit_review'),
    path('delete_review/<review_id>/', delete_review, name='delete_review'),
]
