from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    """ Renders the shopping bag page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Adds a quantity of the product to the shopping bag """
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

    messages.success(request, f'Updated {product.name} ({size.upper()}) to {bag[item_id]["items_by_size"][size]} in the bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """ Adjusts the quantity of a product in the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')  
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id]['items_by_size'][size] = quantity
        messages.success(request, f'Updated {product.name} ({size.upper()}) to {quantity} in the bag.')
    else:
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        messages.success(request, f'Removed {product.name} ({size.upper()}) from the bag.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """ Removes an item from the shopping bag """
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')  
        bag = request.session.get('bag', {})

        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)

        messages.success(request, f'Removed {product.name} ({size.upper()}) from the bag.')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)



