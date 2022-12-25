from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(DjoserUserSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'id', 'email', 'image']


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'id', 'email', 'image']
