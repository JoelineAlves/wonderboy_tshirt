from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product
from decimal import Decimal


def view_bag(request):
    """Renders the shopping bag page with subtotal calculation."""
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    delivery = 5
    grand_total = 0

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

    grand_total = total + delivery

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
    size = request.POST.get('product_size')

    action = request.POST.get('action')
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})

    if item_id in bag:
        if size in bag[item_id]['items_by_size']:
            if action == 'increment':
                quantity += 1
            elif action == 'decrement' and quantity > 1:
                quantity -= 1

            bag[item_id]['items_by_size'][size] = quantity
            messages.success(
                request,
                f'Updated {product.name} ({size.upper()}) to {quantity} in \
                the bag.'
            )
        else:
            messages.error(request, f"Item with size {size} not found \
            in the bag.")
    else:
        messages.error(request, "Item not found in the bag.")

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id, size):
    """Removes an item from the shopping bag."""
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        if item_id in bag:
            if size in bag[item_id]['items_by_size']:
                del bag[item_id]['items_by_size'][size]

                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)

                messages.success(
                    request,
                    f'Removed {product.name} ({size.upper()}) from the bag.'
                )
            else:
                messages.error(request, f'No size {size.upper()} found \
                for this item in the bag.')
        else:
            messages.error(request, 'Item not found in the bag.')

        request.session['bag'] = bag

        return redirect('view_bag')

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect('view_bag')












