from decimal import Decimal
from django.conf import settings

def cart_content(request):

    cart_items = []
    total = 0
    product_count = 0
    delivery = total * 0.20
    
    context = {
        'bag_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context