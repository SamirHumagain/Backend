from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from .serializers import UserRegisterSerializer, OwnerRegisterSerializer, LoginSerializer
from .models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings
class SendOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        import logging
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)
        otp_obj, created = EmailOTP.objects.get_or_create(email=email)
        otp = otp_obj.generate_otp()
        # Send email with error logging
        try:
            send_mail(
                'Your VenueBook OTP',
                f'Your OTP for registration is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            logging.info(f"OTP email sent to {email}")
        except Exception as e:
            logging.error(f"Failed to send OTP email to {email}: {e}")
            return Response({'error': f'Failed to send OTP email: {str(e)}'}, status=500)
        return Response({'success': True, 'message': 'OTP sent to email.'}, status=200)

class VerifyOTPAndRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=400)
        try:
            otp_obj = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            return Response({'error': 'OTP not found for this email.'}, status=400)
        if otp_obj.otp != otp:
            return Response({'error': 'Invalid OTP.'}, status=400)
        otp_obj.is_verified = True
        otp_obj.save()
        # Now register user
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_obj.delete()  # Remove OTP after successful registration
            return Response({'message': 'User registered.'}, status=201)
        return Response(serializer.errors, status=400)
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # optional if frontend uses session auth

            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)

class RegisterOwnerAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OwnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'Owner registered and logged in.'}, status=201)
        return Response(serializer.errors, status=400)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # <-- FIXED
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Logged in successfully.', 'token': token.key ,   "user": {
        "id": user.id,
        "email": user.email,
        "role": getattr(user, 'user_type', None), 
        
    }}, status=200)
        return Response(serializer.errors, status=400)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=200)
