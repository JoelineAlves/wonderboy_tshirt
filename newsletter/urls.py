from django.urls import path

from . import views

urlpatterns = [
    path('', views.newsletter, name='newsletter'),  # Sem o 'newsletter/' duplicado
    path('subscribe/', views.subscribe_to_newsletter, name='subscribe_to_newsletter'),
    path('create-newsletter/', views.create_newsletter, name='create_newsletter'),
    path('edit-newsletter/<int:id>/', views.edit_newsletter, name='edit_newsletter'),
    path('delete-newsletter/<int:id>/', views.delete_newsletter, name='delete_newsletter'),
]