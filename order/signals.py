from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage


@receiver(post_save, sender=Order)
def post_save_send_email(sender, instance, created, *args, **kwargs):
    if created:
        message = '''
            Hello {} {},
            This email is to comfirm your order at pressed by nana
            Below are your order details

            Order Key: {}
            Billing email: {}

            Thank you for using our service.
            '''.format(instance.full_name, instance.surname, instance.order_key, instance.email)
        email = EmailMessage(
            'Order Confirmation',
            message,
            '', 
            [instance.email]
        )
        # EmailThread(email).start()
        email.send(fail_silently=False)
    else:
        print('booking was not created')