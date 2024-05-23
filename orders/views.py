"""
    @author : David Acosta
    Date: 22/05/2024

    Vistas para procesar el pedido

    Django version: 5.0.6
"""
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from cart.cart import Cart

from .forms import OrderCreateForm
from A_DB.models.orders_models import Order, OrderItem


class OrderCreateView(View):
    def get(self, request):
        """
        Renderiza la template que muestra los productos del pedido

        E/S:
            E -> request
            S -> Template con el formulario
        """
        cart = Cart(request)
        form = OrderCreateForm()
        context = {
            'form': form
        }
        return TemplateResponse(request, 'orders/order/create.html', context)

    def post(self, request):
        """
        Crea el pedido con los datos obtenidos del fomulario

        E/S:
            E -> request
            S -> Redirect a la vista de procesamiento de pago
        """
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price']
                )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))


class AdminOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        if not request.user.is_staff:
            # Si el usuario no es personal, redirigir a algún lugar o mostrar un error
            return HttpResponseForbidden("Solo el personal puede acceder a esta vista.")
            # Si el usuario es personal, continuar con el procesamiento de la vista
        order = get_object_or_404(Order, id=order_id)
        return TemplateResponse(request, 'admin/orders/order/detail.html', {'order': order})
