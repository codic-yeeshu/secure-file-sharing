# users/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User
import jwt
from django.conf import settings

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_token = user.verification_token
            return Response({
                'message': 'User registered successfully. Check your email for verification.',
                "token": verification_token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            
            # Generate JWT token
            token = jwt.encode({
                'user_id': user.id,
                'email': user.email,
                'user_type': user.user_type
            }, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                'token': token,
                'user_type': user.user_type
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        
        try:
            
            user = User.objects.get(verification_token=token)
            user.email_verified = True
            user.verification_token = None
            user.save()
            return Response({
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'message': 'Invalid verification token'
            }, status=status.HTTP_400_BAD_REQUEST)