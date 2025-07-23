from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.choices import UserRoles
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
import random
import string
from django.conf import settings

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.JOBSEEKER, blank=True, null=True)
    email = models.EmailField(unique=True , max_length=50, error_messages={'detail': 'Unique email failed'})
    name = models.CharField(max_length=20)
    otp = models.CharField(max_length=6, blank=True, null=True) #923784
    otp_expiry = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    welcome_message = _(
        'Hi, {name}, welcome to Job Portal.\n'
        'Here is your OTP for registration: {otp}\n'
        'This OTP is valid only for 10 minutes, after that you will need to resent OTP.'
    )

    forget_password_message = _(
        'Hi {name}, you have requested for a password reset for your account.\n'
        'Here is your OTP for password reset: {otp}\n'
        'This OTP is valid only for 10 minutes, after that you will need to resend OTP.'
    )
    
    def generate_otp(self):
        otp = ''.join(random.choices(string.digits, k=6)) 
        self.otp = otp
        self.otp_expiry = timezone.now() + timedelta(minutes=15)
        print(f'otp {self.otp}, expiry {self.otp_expiry}')
        self.save()

    # def send_welcome_mail(self):
    #     self.generate_otp()
    #     self.save()
    #     subject = 'Welcome to Job Portal'
    #     message = self.welcome_message.format(
    #         name = self.name,
    #         otp = self.otp
    #     )
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = self.email
    #     send_mail(subject,message, from_email, [recipient_list], fail_silently=False)
    
    # def send_password_mail(self):
    #     # Importing Client here to optimize memory and startup time
    #     # this importing is better than global module importing
    #     from twilio.rest import Client
    #     self.generate_otp()
    #     self.save()
    #     try:
    #         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #         client.messages.create(
    #             body=self.forget_password_message.format(
    #                 name=self.name,
    #                 otp=self.otp
    #             ),
    #             from_=settings.TWILIO_NUMBER,
    #             to=self.phone_number
    #         )    
    #         print(f'message sent to number {self.phone_number}')
    #     except Exception as e:
    #         print(f'Message sending failed with Exception: {e}')
    #         return False
    
    
    def __str__(self):
        return f'{self.name} - ({self.role})'