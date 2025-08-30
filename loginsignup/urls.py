
from django.urls import path
from .views import RegisterUserAPIView, RegisterOwnerAPIView, LoginAPIView, LogoutAPIView, SendOTPAPIView, VerifyOTPAndRegisterAPIView

urlpatterns = [
    path('register/owner/', RegisterOwnerAPIView.as_view(), name='register_owner'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('verify-otp-register/', VerifyOTPAndRegisterAPIView.as_view(), name='verify_otp_register'),
]
