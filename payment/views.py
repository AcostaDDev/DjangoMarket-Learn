import stripe

from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect, reverse, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from A_DB.models.orders_models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentView(View):
    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return TemplateResponse(request, 'payment/process.html', locals())

    def post(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name
                    },
                },
                'quantity': 1,
            })

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)


class PaymentCompletedView(View):
    def get(self, request):
        return TemplateResponse(request, 'payment/completed.html')


class PaymentViewCanceled(View):
    def get(self, request):
        return TemplateResponse(request, 'payment/canceled.html')
