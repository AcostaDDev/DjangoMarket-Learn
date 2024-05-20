from celery import shared_task
from django.core.mail import send_mail, EmailMessage

from A_DB.models.orders_models import Order


@shared_task
def order_paid(order_id):        # No se acepta el objeto en crupo debido a que estos pueden cambiar, asi que se pasa solo el id y así la función se encarga de hacer la consulta a la bbdd
    order = Order.objects.get(id=order_id)
    subject = f'Order id: {order.id}'
    customer_email = order.email
    # pdf_path = generate_invoice_pdf(invoice)

    email = EmailMessage(
        'Tu Factura de Compra',
        f'Gracias {order.first_name} por tu compra. Adjuntamos tu factura en formato PDF.',
        'tusmuertis@elprimo.com',
        [customer_email],
    )
    # email.attach_file(pdf_path)

    mail_sent = email.send()
    return mail_sent
