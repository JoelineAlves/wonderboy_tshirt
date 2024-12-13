from newsletter.models import SubscribeToNewsletter

def newsletter_subscription(request):
    # Inicializa a variável para verificar a inscrição
    subscribed_user = False
    
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Verifica se o e-mail do usuário está na tabela de inscritos na newsletter
        subscribed_user = SubscribeToNewsletter.objects.filter(email=request.user.email).exists()
    
    # Retorna o contexto com a variável 'subscribed_user' que será True ou False
    return {
        'subscribed_user': subscribed_user,
    }
