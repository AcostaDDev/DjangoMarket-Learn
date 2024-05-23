"""
    @author : David Acosta
    Date: 22/05/2024

    Vistas para la tienda

    Django version: 5.0.6
"""
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from A_DB.models.shop_models import Product, Category


class ShopView(View):
    def get(self, request, category_slug: str = None):
        """
        Renderiza la vista de la tienda con los productos y permite filtrarlos por categoría

        E/S:
            E -> request y el slug de la categoria (opcional)
            S -> Renderiza la vista de la tienda
        """
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }

        return TemplateResponse(request, 'shop/product/list.html', context)


class ProductDetailView(View):
    def get(self, request, slug: str, pk: str):
        """
        Renderiza la vista detalle del producto

        E/S:
            E -> request, id y slug del producto
            S -> Renderiza la vista del producto seleccionado
        """
        product = get_object_or_404(Product, slug=slug, id=pk)

        context = {
            'product': product,
        }

        return TemplateResponse(request, 'shop/product/detail.html', context)
