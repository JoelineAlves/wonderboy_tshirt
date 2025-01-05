from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Favorite
from products.models import Product

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # Remove dos favoritos se já existe
        favorite.delete()
        messages.info(request, f"'{product.name}' was removed from your favorites.")
    else:
        # Adiciona aos favoritos
        messages.success(request, f"'{product.name}' was added to your favorites.")

    # Redireciona de volta para a página de detalhe do produto
    return redirect('product_detail', product_id=product.id)

# View to list all the user's favorite products
@login_required
def favorite_list(request):
    print("favorite_list view was called!")  # Debug
    favorites = Favorite.objects.filter(user=request.user)
    print(f"Favorites for user {request.user}: {favorites}")  # Debug
    return render(request, 'favorite/favorite_list.html', {'favorites': favorites})




