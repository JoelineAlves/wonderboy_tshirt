"""
Views for managing products in the store.

These views handle product listing, searching, sorting, 
viewing product details, adding, editing, and deleting products.
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from favorite.models import Favorite
from .models import Product, Category, ProductReview
from .forms import ProductForm


def all_products(request):
    """
    Display all products with support for sorting, filtering, and searching.

    Query Parameters:
        - sort: Field to sort by (e.g., 'name', 'category').
        - direction: Sorting direction ('asc' or 'desc').
        - category: Filter products by category.
        - q: Search term to filter products by name or description.

    Returns:
        Renders the 'products.html' template with filtered product data.
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

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
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
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
    Display details of a specific product, including reviews and favorite status.

    Args:
        product_id (int): The ID of the product to display.

    Returns:
        Renders 'product_detail.html' with product information, reviews, and favorite status.
    """
    product = get_object_or_404(Product, pk=product_id)

    is_favorite = Favorite.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False  
    reviews = product.product_reviews_from_products.all()

    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'is_favorite': is_favorite})


@login_required
def add_product(request):
    """
    Add a new product to the store.

    Only accessible to superusers.

    Returns:
        - Redirects to the product detail page if successful.
        - Renders 'add_product.html' with the form if validation fails.
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
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit an existing product in the store.

    Only accessible to superusers.

    Args:
        product_id (int): The ID of the product to be edited.

    Returns:
        - Redirects to the product detail page if successful.
        - Renders 'edit_product.html' with the form if validation fails.
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
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Delete a product from the store.

    Only accessible to superusers.

    Args:
        product_id (int): The ID of the product to be deleted.

    Returns:
        - Redirects to the product list page if successful.
        - Renders 'delete_product.html' to confirm deletion.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))

    return render(request, "products/delete_product.html", {"product": product})


