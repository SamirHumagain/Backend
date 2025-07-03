from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirmPassword = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    agreeToTerms = serializers.BooleanField(required=False)  # Optional validation

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'confirmPassword', 'agreeToTerms']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs.get('agreeToTerms', True):
            raise serializers.ValidationError({"agreeToTerms": "You must agree to the terms."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        validated_data.pop('agreeToTerms', None)
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class OwnerRegisterSerializer(UserRegisterSerializer):
    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        validated_data.pop('agreeToTerms', None)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.user_type = 'owner'
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include email and password.")
        attrs['user'] = user
        return attrs
