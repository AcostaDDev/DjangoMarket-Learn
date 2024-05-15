from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from A_DB.models.shop_models import Product

from .cart import Cart
from .forms import CartAddProductForm


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True
            })

        return TemplateResponse(request, 'cart/detail.html', {'cart': cart})

    def post(self, request, product_id: int):
        action = request.POST.get('action')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        print(action)

        if not form.is_valid():
            print(form.errors)

        if action == 'add' and form.is_valid():
            print('Hola')
            cd = form.cleaned_data
            cart.add(
                product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override']
            )
        elif action == 'remove':
            cart.remove(product)

        return redirect('cart:cart_detail')
