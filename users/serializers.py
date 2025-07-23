from rest_framework import serializers
from users import models
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from users.tasks import send_welcome_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields='__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user= models.User(
                            username=validated_data['username'],
                            email=validated_data['email'],
                            name = validated_data['name'],
                            role = validated_data['role'],
                            phone_number = validated_data['phone_number']
                        )
        user.set_password(password)
        user.save()
        send_welcome_mail.delay(user.id)
        print('welcome email sent successfully')
        return user
    
class VerifyOTP(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'otp']

class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.User
        fields = ['email', 'new_password', 'confirm_password']
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({'confirm_password': 'Fields do not match'})
        return attrs
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance