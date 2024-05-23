"""
    @author : David Acosta
    Date: 22/05/2024

    Vistas para el carrito de compras

    Django version: 5.0.6
"""
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from A_DB.models.shop_models import Product

from .cart import Cart


class CartView(View):
    def get(self, request):
        """
        Renderiza la template que muestra los productos del carrito

        E/S:
            E -> request
            S -> Template
        """
        return TemplateResponse(request, 'cart/detail.html')

    def post(self, request, product_id: int):
        """
        Añade productos al carrito o los elimina

        E/S:
            E -> request, id del producto
            S -> redirecciona al detalle del carrito
        """
        action = request.POST.get('action')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        print(action)

        if action == 'add':
            cart.add(
                product=product
            )
        elif action == 'remove':
            cart.remove(product)

        return redirect('cart:cart_detail')
