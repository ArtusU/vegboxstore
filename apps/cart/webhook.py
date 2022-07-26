import json
from math import prod
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.order.models import Order
from apps.store.utils import decrement_product_quantity, send_order_confirmation


@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        return HttpResponse(status=404)

    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid_amount = payment_intent.amount / 100
        order.paid = True
        order.save()

        for item in order.items.all():
            product = item.product
            product.num_available -= item.quantity
            product.save()

        # html = render_to_string('order_confirmation.html', {'order': order})
        # send_mail('Order confirmation', 'Your order has been sent.', 'mail@ecf-vegbox.com', ['mail@ecf-vegbox.com', order.email], fail_silently=False, html_message=html)

        send_order_confirmation(order)
        decrement_product_quantity(order)

    return HttpResponse(status=200)
