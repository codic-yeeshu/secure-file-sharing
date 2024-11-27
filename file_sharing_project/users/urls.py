from django.urls import path
from .views import UserRegistrationView, UserLoginView, EmailVerificationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verify'),
]
