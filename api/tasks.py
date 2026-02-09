from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(order_id, user_email):
    subject = f'Order Confirmation - Order #{order_id}'
    message = f'Thank you for your order! Your order ID is {order_id}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    return send_mail(subject, message, from_email, recipient_list)
