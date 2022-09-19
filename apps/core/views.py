from django.shortcuts import render

from apps.store.models import Product
from apps.order.models import Order


def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def frontpage(request):
    products = Product.objects.filter(is_featured=True)
    context = {'list_products': products}
    return render(request, 'frontpage.html', context)


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')