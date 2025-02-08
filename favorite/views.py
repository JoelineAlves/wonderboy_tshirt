from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Favorite
from products.models import Product

@login_required
def toggle_favorite(request, product_id):
    """
    Add or remove a product from the user's favorites.  

    If the product is already in the user's favorites, it is removed.  
    Otherwise, it is added. Displays a success or info message accordingly.  

    Args:  
        request (HttpRequest): The request object containing user information.  
        product_id (int): The ID of the product to be favorited or unfavorited.  

    Returns:  
        HttpResponseRedirect: Redirects to the product detail page.  
    """
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        messages.info(request, f"'{product.name}' was removed from your favorites.")
    else:
        messages.success(request, f"'{product.name}' was added to your favorites.")

    return redirect('product_detail', product_id=product.id)

@login_required
def favorite_list(request):
    """
    Display a list of the user's favorite products.  

    Retrieves all products that the logged-in user has marked as favorites  
    and renders them in the favorite list template.  

    Args:  
        request (HttpRequest): The request object containing user information.  

    Returns:  
        HttpResponse: Renders the 'favorite_list.html' template with the user's favorite products.  
    """
    print("favorite_list view was called!")  
    favorites = Favorite.objects.filter(user=request.user)
    print(f"Favorites for user {request.user}: {favorites}")  
    return render(request, 'favorite/favorite_list.html', {'favorites': favorites})




