from rest_framework import serializers

from Edairy.models import Cow, Calf


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = "__all__"
        ref_name="AnimalManagementCow"


class CalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = "__all__"
        ref_name="AnimalManagementCalf"


class RegisterCalfBirthSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    breed = serializers.CharField(max_length=100)
    sex = serializers.ChoiceField(
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ]
    )
    date_of_birth = serializers.DateField()


class AssignWorkerSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()
