from django.shortcuts import render
from .models import SubscribeToNewsletter

def index(request):
    """ A view to return the index page """
    
    # Verificar se o usuário está autenticado e inscrito na newsletter
    if request.user.is_authenticated:
        subscribed_user = SubscribeToNewsletter.objects.filter(user=request.user).exists()
    else:
        subscribed_user = False  # Se não estiver autenticado, assume-se que não está inscrito

    return render(request, 'home/index.html', {
        'subscribed_user': subscribed_user,  # Passa a variável para o template
    })