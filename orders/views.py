from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from cart.cart import Cart

from .tasks import order_created
from .forms import OrderCreateForm
from A_DB.models.orders_models import Order, OrderItem


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm
        context = {
            'cart': cart,
            'form': form
        }
        return TemplateResponse(request, 'orders/order/create.html', context)

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
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