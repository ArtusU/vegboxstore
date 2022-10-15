import json
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.cart.cart import Cart
from apps.coupon.models import Coupon
from apps.order.models import Order
from apps.order.utils import checkout

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest

from apps.store.utils import decrement_product_quantity, send_order_confirmation

from .models import Product


def checkout_session(request):
    data = json.loads(request.body)
    coupon_code = data['coupon_code']
    coupon_value = 0
    
    if coupon_code != '':
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon.can_use():
            coupon_value = coupon.value
            coupon.use()
    
    cart = Cart(request)
    items = []
    for item in cart:
        product = item['product']
        price = int(product.price * 100)
        if coupon_value > 0:
            price = int(price - (int(price * (int(coupon_value)/100))))
            
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
    
    gateway = data['gateway']
    session = ''
    order_id = ''
    payment_intent = ''
    
    if gateway == 'stripe':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
                                    payment_method_types=['card'],
                                    line_items=items,
                                    mode='payment',
                                    success_url='http://127.0.0.1:8000/cart/success/',
                                    cancel_url='http://127.0.0.1:8000/cart/'
        )
        payment_intent = session.payment_intent
    
    
    orderid = checkout(request, 
                       data['first_name'], 
                       data['last_name'], 
                       data['email'], 
                       data['address'], 
                       data['postcode'], 
                       data['city'], 
                       data['phone']
                       )
    
    total_price = 0.00

    for item in cart:
        product = item['product']
        total_price = total_price + (float(product.price) * int(item['quantity']))

    if coupon_value > 0:
        total_price = total_price * (coupon_value / 100)
    
    if gateway == 'paypal':
        order_id = data['order_id']
        environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
        client = PayPalHttpClient(environment)

        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price
        order.used_coupon = coupon_code

        if response.result.status == 'COMPLETED':
            order.paid = True
            order.payment_intent = order_id
            order.save()

            decrement_product_quantity(order)
            send_order_confirmation(order)
        else:
            order.paid = False
            order.save()
    
    else:
        order = Order.objects.get(id=orderid)
        order.payment_intent = payment_intent
        order.used_coupon = coupon_code
        order.save()
    
    return JsonResponse({'session': session})
        

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
    
    