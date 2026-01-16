from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Management  # use proper class name (usually User)


# User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =Management 
        fields = "__all__"



# Registration Serializer

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Management
        fields = ('username', 'password', 'phone_number')

    def create(self, validated_data):
        user = Management.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )
        return user



# Login Serializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data['user'] = user
        return data
