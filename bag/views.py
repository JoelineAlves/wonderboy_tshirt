from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    """ Renderiza a página do carrinho """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Adiciona uma quantidade do produto ao carrinho """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size')  # ✅ Garantimos que size sempre existe
    bag = request.session.get('bag', {})

    if item_id in bag:
        if size in bag[item_id]['items_by_size']:
            bag[item_id]['items_by_size'][size] += quantity  # ✅ Soma a quantidade
        else:
            bag[item_id]['items_by_size'][size] = quantity
    else:
        bag[item_id] = {'items_by_size': {size: quantity}}

    messages.success(request, f'Atualizado {product.name} ({size.upper()}) para {bag[item_id]["items_by_size"][size]} no carrinho.')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """ Ajusta a quantidade de um produto no carrinho """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')  
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id]['items_by_size'][size] = quantity
        messages.success(request, f'Atualizado {product.name} ({size.upper()}) para {quantity} no carrinho.')
    else:
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        messages.success(request, f'Removido {product.name} ({size.upper()}) do carrinho.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """ Remove um item do carrinho """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')  
        bag = request.session.get('bag', {})

        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)

        messages.success(request, f'Removido {product.name} ({size.upper()}) do carrinho.')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Erro ao remover item: {e}')
        return HttpResponse(status=500)

