from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from users.models import User

#task 1: send welcome email to every new user that registers 
@shared_task
def send_welcome_mail(user_id):
    from users.models import User
    user = User.objects.get(id=user_id)
    user.generate_otp()
    user.save()
    subject = 'Welcome to Job Portal'
    message = user.welcome_message.format(
        name = user.name,
        otp = user.otp
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = user.email
    try:
        send_mail(subject,message, from_email, [recipient_list], fail_silently=False)
    except Exception as e:
        print({'email not sent': str(e)})


#task 2: send otp if a user sends a password forgot request
@shared_task
def send_password_mail(user_id):
    # Importing Client here to optimize memory and startup time
    # this importing is better than global module importing
    from twilio.rest import Client
    from users.models import User
    user = User.objects.get(id=user_id)
    user.generate_otp()
    user.save()
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=user.forget_password_message.format(
                name=user.name,
                otp=user.otp
            ),
            from_=settings.TWILIO_NUMBER,
            to=user.phone_number
        )    
        print(f'message sent to number {user.phone_number}')
    except Exception as e:
        print(f'Message sending failed with Exception: {e}')
        return False
    

@shared_task
def delete_unverified_users():
    deletion_date = timezone.now() - timedelta(days=30)
    users = User.objects.filter(is_verified=False, created_at__gt=deletion_date)
    count_users = users.count()
    users.delete()
    return f'{count_users} have been deleted due to unverification for a month.'