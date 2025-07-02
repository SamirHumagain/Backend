
from django.urls import path
from .views import RegisterUserAPIView, RegisterOwnerAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/user/', RegisterUserAPIView.as_view(), name='register_user'),
    path('register/owner/', RegisterOwnerAPIView.as_view(), name='register_owner'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
