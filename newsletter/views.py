from django.shortcuts import render, redirect, get_object_or_404
from .models import Newsletters, SubscribeToNewsletter
from django.contrib import messages
from .forms import NewsletterForm

# View para inscrição na newsletter
def subscribe_to_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Verifica se o usuário já está inscrito
        if SubscribeToNewsletter.objects.filter(email=email).exists():
            messages.error(request, 'Você já está inscrito na newsletter.')
        else:
            # Tenta obter a newsletter com base no id enviado no formulário
            newsletter_id = request.POST.get('newsletter')
            
            # Verifica se o id da newsletter foi enviado e se a newsletter existe
            if newsletter_id:
                newsletter = get_object_or_404(Newsletters, id=newsletter_id)
                SubscribeToNewsletter.objects.create(email=email, newsletter=newsletter)
                messages.success(request, 'Você se inscreveu com sucesso na newsletter.')
            else:
                messages.error(request, 'Newsletter não selecionada.')
    return redirect('home')


# View para exibir todas as newsletters disponíveis
def newsletter(request):
    newsletters = Newsletters.objects.all()
    template = 'newsletter/newsletter.html'
    context = {
        'newsletters': newsletters
    }
    return render(request, template, context)


# View para criar uma nova newsletter
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter criada com sucesso.')
            return redirect('newsletter')
        else:
            messages.error(request, 'Ocorreu um erro. Por favor, tente novamente.')
    else:
        form = NewsletterForm()

    template = 'newsletter/create_newsletter.html'
    context = {
        'form': form
    }
    
    return render(request, template, context)


# View para editar uma newsletter existente
def edit_newsletter(request, id):
    newsletter = Newsletters.objects.get(id=id)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter atualizada com sucesso.')
            return redirect('newsletter')
        else:
            messages.error(request, 'Ocorreu um erro. Por favor, tente novamente.')
    else:
        form = NewsletterForm(instance=newsletter)

    template = 'newsletter/edit_newsletter.html'
    context = {
        'form': form,
        'newsletter': newsletter
    }
    
    return render(request, template, context)


# View para excluir uma newsletter
def delete_newsletter(request, id):
    newsletter = Newsletters.objects.get(id=id)

    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter excluída com sucesso.')
        return redirect('newsletter')
    
    template = 'newsletter/delete_newsletter.html'
    context = {
        'newsletter': newsletter
    }
    
    return render(request, template, context)

