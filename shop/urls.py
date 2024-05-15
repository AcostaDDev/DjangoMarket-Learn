from django.conf.urls.static import static
from django.urls import path

from djangoProject import settings
from .views import ShopView, ProductDetailView


app_name = 'shop'
urlpatterns = [
    path('', ShopView.as_view(), name='product_list'),
    path('<slug:category_slug>/', ShopView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]