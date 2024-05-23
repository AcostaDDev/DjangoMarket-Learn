'''
    @author : David Acosta
    Date: 22/05/2024

    Vistas para procesar el pago con Stripe

    Django version: 5.0.6
    Stripe version: 2024-04-10
'''


import stripe

from decimal import Decimal

from django.conf import settings
from django.shortcuts import reverse, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.http import JsonResponse

from A_DB.models.orders_models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentView(View):
    def get(self, request):
        """
        Renderiza la template para el proceso de pago

        E/S:
            E -> requesty el id del pedido
            S -> Template y el pedido
        """
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return TemplateResponse(request, 'payment/process.html', locals())

    def post(self, request):
        """
        Manda a Stripe la orden de pago con todos los datos necesarios extraidos del pedido

        E/S:
            E -> request y el id del pedido
            S -> Redirecciona a la vista de pago de stripe
        """
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        session_data = {
            'mode': 'payment',
            'payment_method_types': ['card', 'paypal'],
            # 'shipping_address_collection': {
            #     'allowed_countries': ['US', 'ES']
            # },
            # 'custom_text': {
            #     'shipping_address': {
            #         'message': f'{order.address} -> {order.city}',
            #     }
            # },
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'eur',
                    'product_data': {
                        'name': item.product.name,
                        # 'images': [f'{item.product.get_image_url()}']
                    },
                },
                'quantity': 1,
            })

        session = stripe.checkout.Session.create(**session_data)
        # return JsonResponse({
        #     'id': session.id
        # })
        return redirect(session.url, code=303)


class PaymentCompletedView(View):
    def get(self, request):
        """
        Renderiza la template de pago exitoso

        E/S:
            E -> request
            S -> Template
        """
        return TemplateResponse(request, 'payment/completed.html')


class PaymentViewCanceled(View):
    def get(self, request):
        """
        Renderiza la template de pago cancelado

        E/S:
            E -> request
            S -> Template
        """
        return TemplateResponse(request, 'payment/canceled.html')
