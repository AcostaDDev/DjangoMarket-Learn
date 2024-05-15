from django.urls import path

from .views import PaymentView, PaymentViewCanceled, PaymentCompletedView
from . import webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', PaymentView.as_view(), name='process'),
    path('completed/', PaymentCompletedView.as_view(), name='completed'),
    path('canceled/', PaymentViewCanceled.as_view(), name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webook'),
]
