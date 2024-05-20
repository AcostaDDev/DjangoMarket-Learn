from django import forms

from A_DB.models.orders_models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'postal_code', 'city']
