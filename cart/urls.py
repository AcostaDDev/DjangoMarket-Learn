from django.urls import path
from .views import CartView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartView.as_view(), name='cart_remove'),
]

