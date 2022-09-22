from django.conf import settings
from django.shortcuts import render
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        product_url = '/%s/%s/' % (product.category.slug, product.slug) 
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'product_url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.thumbnail.url, product_url, product.num_available)

        productsstring = productsstring + b
        
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
    else:
        first_name = last_name = email = ''
    
    context = {
        'cart': cart,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'pub_key': settings.STRIPE_PUBLISHABLE_KEY,
        'productsstring': productsstring.rstrip(',')
        }
    
    return render(request, 'cart.html', context)


def success(request):
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'success.html')
