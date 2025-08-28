from rest_framework import serializers
from .models import CustomUser

class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'address', 'profile_image', 'user_type']
