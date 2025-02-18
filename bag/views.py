from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """Renders the shopping bag page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Adds a quantity of the product to the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size')
    bag = request.session.get('bag', {})

    if item_id in bag:
        if size in bag[item_id]['items_by_size']:
            bag[item_id]['items_by_size'][size] += quantity
        else:
            bag[item_id]['items_by_size'][size] = quantity
    else:
        bag[item_id] = {'items_by_size': {size: quantity}}

    messages.success(
        request,
        f'Updated {product.name} ({size.upper()}) to '
        f'{bag[item_id]["items_by_size"][size]} in the bag.'
    )

    request.session['bag'] = bag
    return redirect(redirect_url)


def update_bag(request):
    """ Atualiza a quantidade do produto no carrinho via AJAX """
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        size = request.POST.get('size', None)
        bag = request.session.get('bag', {})

        product = get_object_or_404(Product, pk=product_id)

        if quantity > 0:
            bag[product_id] = {'quantity': quantity, 'size': size}
        else:
            bag.pop(product_id, None)

        request.session['bag'] = bag

        # Calcula o novo total do carrinho
        new_total = sum(item['quantity'] * product.price for item in bag.values())

        return JsonResponse({'success': True, 'new_total': new_total})


def adjust_bag(request, item_id):
    """Adjusts the quantity of a product in the shopping bag via AJAX."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id]['items_by_size'][size] = quantity
        request.session['bag'] = bag
        subtotal = product.price * quantity  # Calcula o subtotal
        return JsonResponse({'subtotal': subtotal, 'quantity': quantity})  # Retorna JSON
    else:
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        request.session['bag'] = bag
        return JsonResponse({'removed': True})  # Retorna JSON informando remoção


def remove_from_bag(request, item_id):
    """Removes an item from the shopping bag."""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')
        bag = request.session.get('bag', {})

        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)

        messages.success(
            request,
            f'Removed {product.name} ({size.upper()}) from the bag.'
        )
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)




