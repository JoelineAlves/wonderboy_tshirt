from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductReview
from .forms import ProductReviewForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

# List all reviews for a specific product
def all_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.product_reviews_from_reviews.all()  

    for review in reviews:
        review.stars = range(int(review.rating))
        review.half_star = review.rating - int(review.rating) > 0

    template = 'reviews/all_reviews.html'
    context = {'product': product, 'reviews': reviews}
    return render(request, template, context)

# Add a new review
@login_required
def add_review(request, product_id):
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
            messages.error(request, 
                'There was an error submitting your review. Please try again.')
    else:
        form = ProductReviewForm()

    template = 'reviews/add_review.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)

# Edit an existing review
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    if request.user != review.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', product_id=review.product.id)
        else:
            messages.error(request, 
                'There was an error updating your review. Please try again.')
    else:
        form = ProductReviewForm(instance=review)

    template = 'reviews/edit_review.html'
    context = {
        'form': form,
        'review': review,
        'product': review.product  
    }
    return render(request, template, context)

# Delete a review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)

    if request.user != review.user:
        raise PermissionDenied

    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('product_detail', product_id=product_id)


