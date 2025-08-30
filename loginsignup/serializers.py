from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirmPassword = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    agreeToTerms = serializers.BooleanField(required=False)  # Optional validation
    role = serializers.CharField(required=False, default='user')

    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'confirmPassword', 'agreeToTerms', 'role', 'address', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs.get('agreeToTerms', True):
            raise serializers.ValidationError({"agreeToTerms": "You must agree to the terms."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        validated_data.pop('confirmPassword')
        validated_data.pop('agreeToTerms', None)
        address = validated_data.pop('address', '')
        phone = validated_data.pop('phone', '')
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            address=address,
            phone=phone
        )
        user.user_type = role
        user.save()
        return user


class OwnerRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirmPassword = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    agreeToTerms = serializers.BooleanField(required=True)

    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'confirmPassword', 'agreeToTerms', 'address', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs.get('agreeToTerms', False):
            raise serializers.ValidationError({"agreeToTerms": "You must agree to the terms."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        validated_data.pop('agreeToTerms', None)
        address = validated_data.pop('address', '')
        phone = validated_data.pop('phone', '')
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            address=address,
            phone=phone
        )
        user.user_type = 'venue_owner' 
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
