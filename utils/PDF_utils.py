# utils.PDF_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_invoice_pdf(order):
    file_path = f'/tmp/invoice_{order.id}.pdf'
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, f"Factura ID: {order.id}")
    c.drawString(100, 730, f"Cliente: {order.email}")
    c.drawString(100, 710, f"Monto: {order.total_amount}")

    # Agregar más detalles según sea necesario

    c.showPage()
    c.save()
    return file_path
