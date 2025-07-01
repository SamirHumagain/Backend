from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from .serializers import UserRegisterSerializer, OwnerRegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token  # ✅ import Token model
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # optional if frontend does session
            token, _ = Token.objects.get_or_create(user=user)  # ✅ create token
            return Response({'message': 'User registered and logged in.', 'token': token.key}, status=201)
        return Response(serializer.errors, status=400)

class RegisterOwnerAPIView(APIView):
    def post(self, request):
        serializer = OwnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)  # ✅ create token
            return Response({'message': 'Owner registered and logged in.', 'token': token.key}, status=201)
        return Response(serializer.errors, status=400)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)  # ✅ return token
            return Response({'message': 'Logged in successfully.', 'token': token.key}, status=200)
        return Response(serializer.errors, status=400)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # ✅ delete token
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=200)
