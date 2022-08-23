import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.cart.cart import Cart
from apps.order.models import Order, OrderItem
from apps.order.utils import checkout

from .models import Product


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
    
    