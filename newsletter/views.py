from django.shortcuts import render, redirect
from .models import Newsletters, SubscribeToNewsletter
from django.contrib import messages
from django.utils import timezone  # Importando timezone para usar a data e hora atuais
from .forms import NewsletterForm

# Create your views here.
def subscribe_to_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if SubscribeToNewsletter.objects.filter(email=email).exists():
            messages.error(request, 'You have already subscribed to the newsletter.')
        else:
            # Agora, vamos definir explicitamente o campo 'date_added'
            SubscribeToNewsletter.objects.create(
                email=email,
                date_added=timezone.now()  # Definindo explicitamente o valor de 'date_added'
            )
            messages.success(request, 'You have successfully subscribed to the newsletter.')
    return redirect('home')


def newsletter(request):
    newsletters = Newsletters.objects.all()
    template = 'newsletter/newsletter.html'
    context = {
        'newsletters': newsletters
    }
    return render(request, template, context)


def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter created successfully.')
            return redirect('newsletter')
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        form = NewsletterForm()

    template = 'newsletter/create_newsletter.html'
    context = {
        'form': form,
        'newsletter': Newsletters.objects.all()
    }
    
    return render(request, template, context)


def edit_newsletter(request, id):
    newsletter = Newsletters.objects.get(id=id)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated successfully.')
            return redirect('newsletter')
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        form = NewsletterForm(instance=newsletter)

    template = 'newsletter/edit_newsletter.html'
    context = {
        'form': form,
        'newsletter': newsletter
    }
    
    return render(request, template, context)


# View for deleting a newsletter from the database
def delete_newsletter(request, id):
    newsletter = Newsletters.objects.get(id=id)

    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter deleted successfully.')
        return redirect('newsletter')
    
    template = 'newsletter/delete_newsletter.html'
    context = {
        'newsletter': newsletter
    }
    
    return render(request, template, context)
