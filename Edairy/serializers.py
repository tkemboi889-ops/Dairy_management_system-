from .models import Owner,Worker,Cow,Calf,Milk,Feed
from rest_framework import serializers
from datetime import date
#creating serializers for models


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        # Email uniqueness check 
        if email:
            queryset = Owner.objects.filter(email=email)

            # Exclude current instance during update
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    {"email": "This email is already registered."}
                )

        #Phone number validation
        if phone_number:
            if not phone_number.isdigit():
                raise serializers.ValidationError(
                    {"phone_number": "Phone number must contain only digits."}
                )

            if len(phone_number) != 10:
                raise serializers.ValidationError(
                    {"phone_number": "Phone number must be exactly 10 digits."}
                )

        return attrs



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
    def validate_age(self,value):
         if value <=0:
             raise serializers.ValidationError({
                 'message': 'age should be above one year'
             })
         return value



class CalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = '__all__'

        def validate_age(self,value):
         if value <=1:
             raise serializers.ValidationError({
                 'message': 'This is an incalf already ready served'
             })
         return value


class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = '__all__'
    def validate_date_collected(self,value):
        if value > date.today():
         raise serializers.ValidationError({
            'message':'milk date cannot be in future'

        })
        return value



class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'
    def validate_store_number(self,value):
        if value <=0:
            raise serializers.ValidationError({
                'message': 'store number should be a positive numbers starting from 1'
            })
        return value

