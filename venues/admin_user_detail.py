from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AdminUserDetail(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        updated = False
        for field in ['is_active', 'name', 'email', 'phone', 'address', 'profile_image']:
            if field in data:
                setattr(user, field, data[field])
                updated = True
        if updated:
            user.save()
        return Response({'id': user.id, 'is_active': user.is_active, 'name': user.name, 'email': user.email})

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)
