"""
Views for managing user profiles and order history.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def profile(request):
    """
    Display and update the user's profile.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the profile page with the user's information.

    Functionality:
        - Retrieves the authenticated user's profile.
        - If the request method is POST, updates the profile with the submitted form data.
        - If the form is valid, saves changes and displays a success message.
        - If the form is invalid, displays an error message.
        - If the request is GET, loads the profile form with existing user data.
        - Retrieves the user's order history.
        - Renders the profile page with the profile form and order history.

    Template:
        - profiles/profile.html

    Context:
        - form (UserProfileForm): The form for updating the user's profile.
        - orders (QuerySet): The list of orders associated with the user.
        - on_profile_page (bool): A flag to indicate the user is on the profile page.
    """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Display a past order confirmation.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        order_number (str): The unique identifier for the order.

    Returns:
        HttpResponse: Renders the order confirmation page.

    Functionality:
        - Retrieves the order using the provided order number.
        - Displays an informational message that the order confirmation was previously sent.
        - Renders the checkout success page with order details.

    Template:
        - checkout/checkout_success.html

    Context:
        - order (Order): The retrieved order object.
        - from_profile (bool): A flag indicating the user accessed this from the profile page.
    """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
