from .models import Owner,Worker,Cow,Calf,Milk,Feed
from rest_framework import serializers
#creating serializers for models

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'
        
    def validate_email(self, value):
        if Owner.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value 


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'


class CalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = '__all__'


class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = '__all__'


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'
