from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_content(request):

    cart_items = []
    order_total = 0
    product_count = 0
    total_product_count = 0
    delivery = order_total * 0.20

    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, ean_code=item_id)
        order_total += quantity * product.price
        total_product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })
        product_count = len(cart_items)
    
    context = {
        'cart_items': cart_items,
        'product_count': product_count,
        'order_total': order_total,
        'total_product_count': total_product_count,
        'delivery': delivery,
    }

    return context