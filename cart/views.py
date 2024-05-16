from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from A_DB.models.shop_models import Product

from .cart import Cart


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return TemplateResponse(request, 'cart/detail.html', {'cart': cart})

    def post(self, request, product_id: int):
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
