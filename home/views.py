from django.shortcuts import render


# Create your views here.
def home(request):
    """ Home view """
    return render(request, 'home/home.html')