
"""
    @author : David Acosta
    Date: 22/05/2024

    Clase para manejar y definir el comportamiento del carrito de compras

    Django version: 5.0.6
"""
from decimal import Decimal
from django.conf import settings

from A_DB.models.shop_models import Product


class Cart:
    def __init__(self, request):
        """
        Obtiene el carrito de compras, si no existe lo crea

        E/S:
            E -> request
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Itera sobre el carrito de compras haicendo la estructura de los items como un diccionario

        E/S:
            E -> self
            S -> carrito como diccionario
        """
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
        """
        Cuenta la cantidad de items en el carrito

        E/S:
            E -> self
            S -> Cantidad de items en el carrito
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product: Product, quantity=1):
        """
        Agrega un producto (item) al carrito guardando la sesión

        E/S:
            E -> self, product, quantity
            S -> None
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 1,
                'price': str(product.price)
            }
        self.save()

    def save(self):
        """
        Guarda la sesión

        E/S:
            E -> self
            S -> None
        """
        self.session.modified = True

    def remove(self, product: Product):
        """
        Elimina un producto (item) del carrito

        E/S:
            E -> self, product
            S -> None
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Limpia el carrito de compras eliminando la sesión

        E/S:
            E -> self
            S -> None
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calcula el total del carrito de compras

        E/S:
            E -> self
            S -> Total del carrito de compras
        """
        return sum(Decimal(item['price']) for item in self.cart.values())
