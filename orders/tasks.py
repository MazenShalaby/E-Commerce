from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Order

# create your tasks here.


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification
    when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = "Order Placement"
    message = f"Thank you for your order!\nYour order has been successfully placed.\nOrder ID: {order.order_id}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.email]
    mail_sent = send_mail(subject, message, from_email, recipient_list)
    
    return mail_sent