import json
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.cart.cart import Cart
from apps.order.models import Order, OrderItem
from apps.order.utils import checkout

from .models import Product


def checkout_session(request):
    cart = Cart(request)
    items = []
    for item in cart:
        product = item['product']
        price = int(product.price)
        obj = {
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': price
            },
            'quantity': item['quantity'],
        }
        items.append(obj)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
                                payment_method_types=['card'],
                                line_items=items,
                                mode='payment',
                                success_url='http://127.0.0.1:8000/cart/success/',
                                cancel_url='http://127.0.0.1:8000/cart/'
    )
    payment_intent = session.payment_intent
    data = json.loads(request.body)
    orderid = checkout(request, 
                       data['first_name'], 
                       data['last_name'], 
                       data['email'], 
                       data['address'], 
                       data['postcode'], 
                       data['city'], 
                       data['phone']
                       )
    order = Order.objects.get(id=orderid)
    order.payment_intent = payment_intent
    order.save()
    
    return JsonResponse({'session': session})
    

def api_checkout(request):
    cart = Cart(request)
    data = json.loads(request.body)
    orderid = checkout(request, 
                       data['first_name'], 
                       data['last_name'], 
                       data['email'], 
                       data['address'], 
                       data['postcode'], 
                       data['city'], 
                       data['phone']
                       )
    
    paid = True
    
    if paid == True:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()
        cart.clear()
        
    return JsonResponse({'success': True})
        

def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    
    return JsonResponse(jsonresponse)


def api_remove_from_cart(request):
    data = json.loads(request.body)
    product_id = str(data['product_id'])
    
    cart = Cart(request)
    cart.remove(product_id)
    
    return JsonResponse({'success': True})
    
    