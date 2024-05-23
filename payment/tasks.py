'''
    @author : David Acosta
    Date: 22/05/2024

    Tareas a realizar por Celery: Envío de correos

    Django version: 5.0.6
    Celery version: 5.4.0
'''

from celery import shared_task
from django.core.mail import send_mail

from A_DB.models.orders_models import Order


@shared_task
def order_paid(order_id):        # No se acepta el objeto en crupo debido a que estos pueden cambiar, asi que se pasa solo el id y así la función se encarga de hacer la consulta a la bbdd
    '''
    Envia un correo al usuario cuando el pedido ha sido pagado

    E/S:
        E -> order_id
        S -> Correo enviado
    '''
    order = Order.objects.get(id=order_id)
    subject = f'Order id: {order.id}'
    message = f"""
                Dear {order.first_name},
                You have successfully paid an order.
                Your order id is {order.id}.
                """
    mail_sent = send_mail(subject=subject, message=message, from_email='admin@myshop.com', recipient_list=[order.email])
    return mail_sent
