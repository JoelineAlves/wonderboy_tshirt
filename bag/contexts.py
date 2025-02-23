from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Retrieves shopping bag contents, calculates total, delivery charge,
    and grand total, then returns a context dictionary.

    Args:
        request (HttpRequest): The request containing session data.

    Returns:
        dict: A dictionary with:
            - 'bag_items' (list): Bag items with product details.
            - 'total' (Decimal): Total cost of products.
            - 'product_count' (int): Total number of products.
            - 'delivery' (Decimal): Delivery charge.
            - 'free_delivery_delta' (Decimal): Amount needed for free delivery.
            - 'free_delivery_threshold' (Decimal): Minimum for free delivery.
            - 'grand_total' (Decimal): Final total including delivery.
    """

    bag_items = []
    total = Decimal(0)
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            # Quando é uma quantidade simples
            total += item_data * product.price
            product_count += item_data
            bag_items.append(
                {
                    "item_id": item_id,
                    "quantity": item_data,
                    "product": product,
                    "sub_total": item_data * product.price,  # Calculando o subtotal
                }
            )
        else:
            # Quando é um dicionário com diferentes tamanhos
            for size, quantity in item_data["items_by_size"].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                        "sub_total": quantity * product.price,  # Correção aqui, multiplicando a quantidade
                    }
                )

    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD
    std_delivery_pct = settings.STANDARD_DELIVERY_PERCENTAGE

    if total < free_delivery_threshold:
        delivery = total * Decimal(std_delivery_pct / 100)
        free_delivery_delta = free_delivery_threshold - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = Decimal(0)

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": free_delivery_threshold,
        "grand_total": grand_total,
    }

    return context

