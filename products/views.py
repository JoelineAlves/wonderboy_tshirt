"""
Views for managing products in the store.

These views handle product listing, searching, sorting,
viewing product details, adding, editing, and deleting products.
"""

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from favorite.models import Favorite
from .models import Product, Category
from .forms import ProductForm
from reviews.models import ProductReview


def all_products(request):
    """
    Display all products with support for sorting, filtering, and searching.
    """
    products = Product.objects.all()
    query, categories, sort, direction = None, None, None, None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter \
                any search criteria!")
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Display details of a specific product, including reviews and favorites.
    """
    product = get_object_or_404(Product, pk=product_id)

    is_favorite = (
        Favorite.objects.filter(user=request.user, product=product).exists()
        if request.user.is_authenticated
        else False
    )
    reviews = product.product_reviews_from_products.all()

    return render(
        request,
        'products/product_detail.html',
        {'product': product, 'reviews': reviews, 'is_favorite': is_favorite},
    )


@login_required
def add_product(request):
    """
    Add a new product to the store (Superuser only).
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(request, 'Failed to add product. \
        Ensure the form is valid.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """
    Edit an existing product in the store (Superuser only).
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(request, 'Failed to update product. \
        Ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(
        request, 'products/edit_product.html',
        {'form': form, 'product': product}
    )


@login_required
def delete_product(request, product_id):
    """
    Delete a product from the store (Superuser only).
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))

    return render(request, "products/delete_product.html",
                  {"product": product})

