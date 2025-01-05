from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('list/', views.favorite_list, name='favorite_list'),
]
