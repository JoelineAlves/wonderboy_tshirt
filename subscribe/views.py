from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubscribeForm


def subscribe(request):
    """
    Handle user subscription form submission.

    If the request method is POST, validate the submitted form data. 
    If valid, save the subscription, display a success message, 
    and reset the form. Otherwise, show the form again.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the subscription page with the form.
    """
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)

        if subscribe_form.is_valid():
            subscribe_form.save()
            messages.success(request, 'You have successfully subscribed!')

            subscribe_form = SubscribeForm()
    else:
        subscribe_form = SubscribeForm()

    template = 'subscribe/subscribe.html'
    context = {
        'subscribe_form': subscribe_form,
    }

    return render(request, template, context)

