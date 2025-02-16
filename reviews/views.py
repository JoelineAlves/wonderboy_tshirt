from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductReview
from .forms import ProductReviewForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def all_reviews(request, product_id):
    """
    Display all reviews for a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product whose reviews \
        are being retrieved.

    Returns:
        HttpResponse: Renders the template displaying all reviews \
        for the product.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = product.product_reviews_from_reviews.all()

    # Prepare star ratings for template rendering
    for review in reviews:
        review.stars = range(int(review.rating))
        review.half_star = review.rating - int(review.rating) > 0

    template = 'reviews/all_reviews.html'
    context = {'product': product, 'reviews': reviews}
    return render(request, template, context)


@login_required
def add_review(request, product_id):
    """
    Allow an authenticated user to submit a review for a product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product for which the review \
        is being submitted.

    Returns:
        HttpResponseRedirect: Redirects to the product detail page upon \
        successful submission.
        HttpResponse: Renders the review form again if validation fails.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'There was an error submitting your \
            review. Please try again.')
    else:
        form = ProductReviewForm()

    template = 'reviews/add_review.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    """
    Allow an authenticated user to edit their own review.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The ID of the review to be edited.

    Returns:
        HttpResponseRedirect: Redirects to the product detail page upon \
        successful update.
        HttpResponse: Renders the edit review form again if validation fails.
        HttpResponseForbidden: Raises a PermissionDenied error if the user \
        is not the owner of the review.
    """
    review = get_object_or_404(ProductReview, id=review_id)

    # Ensure only the review owner can edit the review
    if request.user != review.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', product_id=review.product.id)
        else:
            messages.error(request, 'There was an error updating your \
            review. Please try again.')
    else:
        form = ProductReviewForm(instance=review)

    template = 'reviews/edit_review.html'
    context = {
        'form': form,
        'review': review,
        'product': review.product
    }
    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    Allow an authenticated user to delete their own review.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The ID of the review to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the product detail page after \
        successful deletion.
        HttpResponseForbidden: Raises a PermissionDenied error if the user \
        is not the owner of the review.
    """
    review = get_object_or_404(ProductReview, id=review_id)

    # Ensure only the review owner can delete the review
    if request.user != review.user:
        raise PermissionDenied

    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('product_detail', product_id=product_id)




