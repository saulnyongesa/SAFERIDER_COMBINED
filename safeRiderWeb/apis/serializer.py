from rest_framework import serializers
from base.models import *


# Create a model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'second_name', 'last_name', 'username', 'email', 'phone_number', 'password')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id_number', 'first_name', 'second_name', 'last_name', 'email', 'phone_number')


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ('emergency_name', 'email', 'phone_number')

