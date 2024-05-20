# tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from A_DB.models.orders_models import Order
from utils.PDF_utils import generate_invoice_pdf


@shared_task
def order_paid(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order id: {order.id}'
    customer_email = order.email

    # Generar el PDF
    pdf_path = generate_invoice_pdf(order)

    email = EmailMessage(
        'Tu Factura de Compra',
        f'Gracias {order.first_name} por tu compra. Adjuntamos tu factura en formato PDF.',
        'tusmuertis@elprimo.com',
        [customer_email],
    )

    # Adjuntar el archivo PDF
    email.attach_file(pdf_path)
    mail_sent = email.send()
    return mail_sent

