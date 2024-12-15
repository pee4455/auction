from rest_framework import serializers
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email', 'is_superuser']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 