from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('cart', {})
    if not bag:
        messages.error(request, "There's nothing in your shopping cart at this moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KHU9II4JiRbfrjT9Y46o0Tw6SbcLz6wYUCSxZsWxwIh5ur78EhPk7uDxWKmIx60XM3gBueLgEtJwolcAgOAjTbo00KrdJpRkv',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
    