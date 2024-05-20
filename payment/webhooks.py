# views.py
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from A_DB.models.orders_models import Order
from cart.cart import Cart
from .tasks import order_paid

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        cart = Cart(request)
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
                order.paid = True
                order.stripe_id = session.payment_intent
                order.save()
                order_paid.delay(order.id)
                cart.clear()
            except Order.DoesNotExist:
                return HttpResponse(status=404)

    return HttpResponse(status=200)

