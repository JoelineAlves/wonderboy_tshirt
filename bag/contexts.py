from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """
    Retrieves the contents of the shopping bag from the session, calculates the total cost,  
    delivery charge, and grand total, and returns a context dictionary for use in templates.  

    The function iterates through the items in the shopping bag, retrieves product details,  
    and calculates the total price and quantity of products. It also determines whether a  
    delivery charge applies and computes the remaining amount needed to qualify for free delivery.  

    Args:  
        request (HttpRequest): The HTTP request object containing session data, including the shopping bag.  

    Returns:  
           dict: A dictionary containing the following details:  
               - 'bag_items' (list): A list of dictionaries, each representing an item in the bag,  
                 including product details, quantity, and size (if applicable).  
               - 'total' (Decimal): The total cost of all products in the shopping bag.  
               - 'product_count' (int): The total number of products in the shopping bag.  
               - 'delivery' (Decimal): The delivery charge based on the total cost.  
               - 'free_delivery_delta' (Decimal): The amount needed to qualify for free delivery.  
               - 'free_delivery_threshold' (Decimal): The minimum total cost required for free delivery.  
               - 'grand_total' (Decimal): The final total cost, including the delivery charge if applicable.  
    """
    


    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context