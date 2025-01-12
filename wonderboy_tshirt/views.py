# your_app/views.py
from django.shortcuts import render

def wonderboytshirt_404_view(request, exception):
    return render(request, '404.html', status=404)