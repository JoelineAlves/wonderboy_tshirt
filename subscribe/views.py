from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubscribeForm


def subscribe(request):
    # Check if the form has been submitted
    if request.method == 'POST':
        # Create a SubscribeForm instance with the submitted data
        subscribe_form = SubscribeForm(request.POST)

        # Check if the form is valid
        if subscribe_form.is_valid():
            # Save the form data to the database
            subscribe = subscribe_form.save()

            # Display a success message to the user
            messages.success(request, 'You have successfully subscribed!')

            # Optionally, you can clear the form after successful submission
            subscribe_form = SubscribeForm()
    else:
        # If the form has not been submitted, create an empty SubscribeForm
        subscribe_form = SubscribeForm()

    # Set the template file for rendering
    template = 'subscribe/subscribe.html'

    # Prepare the context to be passed to the template
    context = {
        'subscribe_form': subscribe_form,
    }

    # Render the template with the provided context
    return render(request, template, context)
