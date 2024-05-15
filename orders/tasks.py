from celery import shared_task
from django.core.mail import send_mail

from A_DB.models.orders_models import Order


@shared_task
def order_created(order_id):        # No se acepta el objeto en crupo debido a que estos pueden cambiar, asi que se pasa solo el id y así la función se encarga de hacer la consulta a la bbdd
    order = Order.objects.get(id=order_id)
    subject = f'Order id: {order.id}'
    message = f"""
                Dear {order.first_name},
                You have successfully placed an order.
                Your order id is {order.id}.
                """
    mail_sent = send_mail(subject=subject, message=message, from_email='admin@myshop.com', recipient_list=[order.email])
    return mail_sent
