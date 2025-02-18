from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """Renders the shopping bag page with subtotal calculation."""
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    delivery = 5  # Example: fixed delivery fee
    grand_total = 0

    # Loop through items in the bag
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        for size, quantity in item_data['items_by_size'].items():
            sub_total = product.price * quantity
            total += sub_total
            bag_items.append({
                'product': product,
                'quantity': quantity,
                'size': size,
                'sub_total': sub_total,
            })

    grand_total = total + delivery  # Calculate grand total including delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return render(request, 'bag/bag.html', context)


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


def adjust_bag(request, item_id):
    """Adjusts the quantity of a product in the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id]['items_by_size'][size] = quantity
        messages.success(
            request,
            f'Updated {product.name} ({size.upper()}) to {quantity} in the bag.'
        )
    else:
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        messages.success(
            request,
            f'Removed {product.name} ({size.upper()}) from the bag.'
        )

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


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







