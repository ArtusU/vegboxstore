from django.conf import settings
from django.shortcuts import render
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    productsstring = ""

    for item in cart:
        product = item["product"]
        product_url = "/%s/%s/" % (product.category.slug, product.slug)
        b = (
            "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'product_url': '%s', 'num_available': '%s'},"
            % (
                product.id,
                product.title,
                product.price,
                item["quantity"],
                item["total_price"],
                product.get_thumbnail,
                product_url,
                product.num_available,
            )
        )

        productsstring = productsstring + b

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        postcode = request.user.userprofile.postcode
        city = request.user.userprofile.city
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = postcode = city = phone = ""

    context = {
        "cart": cart,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "address": address,
        "postcode": postcode,
        "city": city,
        "phone": phone,
        "pub_key": settings.STRIPE_PUBLISHABLE_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID,
        "productsstring": productsstring.rstrip(","),
    }

    return render(request, "cart.html", context)


def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request, "success.html")
