from .models import farm_manager,Worker,Cow,Calf,Milk,Feed
from rest_framework import serializers

from datetime import date, datetime  
from django.utils import timezone
#creating serializers for models


class farm_managerSerializer(serializers.ModelSerializer):
    class Meta:
        model = farm_manager
        fields = '__all__'

    # Inside Edairy/serializers.py

class farm_managerSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = farm_manager
        fields = ['id', 'user', 'phone_number', 'email'] 

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        if email:
            # Look up via the related user profile relationship
            queryset = farm_manager.objects.filter(user__email=email)

            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    {"email": "This email is already registered."}
                )

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




class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = '__all__'

    def validate_date_collected(self, value):
        # 1. If it's a datetime object (with time/timezone), safely get the date portion
        if isinstance(value, datetime):
            if timezone.is_aware(value):
                value = timezone.localdate(value)
            else:
                value = value.date()
                
        # 2. If value arrives as a string representation, cast it cleanly
        elif isinstance(value, str):
            value = date.fromisoformat(value)

        # 3. Perform the direct date comparison
        if value > date.today():
            raise serializers.ValidationError(
                'milk date cannot be in future'
            )
            
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
        ref_name="EdairyCow"
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

