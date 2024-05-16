from decimal import Decimal
from django.conf import settings

from A_DB.models.shop_models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()  # --> Crea una copia del diccionario para poder trabajar sobre él

        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item
            # --> Yield es un generador que devuelve el diccionario anterior con los valores añadidos y
            # actualizados
            # --> Yield consume cpu en tiempo de ejecución, un iterador normal consume memoria ram

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product: Product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 1,
                'price': str(product.price)
            }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())
