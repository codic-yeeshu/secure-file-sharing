# users/serializers.py
from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
import uuid
import jwt
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_type']

    def create(self, validated_data):
        # Generate verification token
        verification_token = str(uuid.uuid4())
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            verification_token=verification_token
        )

        # Send verification email
        verification_link = f"{settings.BACKEND_URL}/api/users/verify-email/{verification_token}"
        send_mail(
            'Verify Your Email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Custom login validation logic
        user = User.objects.filter(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.email_verified:
            raise serializers.ValidationError("Email not verified")
        
        return data