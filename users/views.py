from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from users.tasks import send_welcome_mail, send_password_mail

from users.models import User
from users.serializers import UserSerializer, VerifyOTP, ResetPasswordRequestSerializer, ResetPasswordSerializer

# Create your views here.

class UserViewset(GenericViewSet, CreateModelMixin):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = []
    http_method_names = ['post']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'User created successfully': serializer.data}, status=status.HTTP_201_CREATED)
    
    @action(
        detail=False,
        methods=['post'],
        serializer_class=VerifyOTP,
        url_path='verify-otp'
    )
    def verify_user(self,request):
        user = get_object_or_404(User, email=request.data['email'])
        if user.otp == request.data['otp'] and user.otp_expiry > timezone.now():
            user.otp = ''
            user.otp_expiry = None
            user.is_verified = True
            user.save()
            return Response({'detail':'OTP verified!'}, status=status.HTTP_200_OK)
        elif user.otp != request.data['otp']: 
            Response({'detail':'Your otp is not valid. Please enter the correct OTP or ask for another one.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'detail':'Your OTP has been expired. Please ask for the otp to be sent again.'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(
        detail=False,
        methods=['post'],
        serializer_class = ResetPasswordRequestSerializer,
        url_path='request-password-reset'
    )
    def request_password_reset(self, request):
        user = get_object_or_404(User, email=request.data['email'])   
        send_password_mail.delay(user.id)    
        user.is_verified = False
        print(f'otp {user.otp} sent to {user.phone_number}') 
        user.save()
        return Response({'detail':'Password reset request has been sent to your registered phone number'}, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=['post'],
        serializer_class = ResetPasswordSerializer,
        url_path='reset-password'
    )
    def reset_password(self, request):
        user = get_object_or_404(User, email=request.data['email']) #when a model is given here, serializer update method is called rather than create method
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Your password has been reset. Please login with your new password!', status=status.HTTP_200_OK)

        



