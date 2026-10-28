from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from Edairy.models import Cow, Worker
from .serializers import (
    CowSerializer,
    CalfSerializer,
    RegisterCalfBirthSerializer,
    AssignWorkerSerializer,
)
from .services.animal_service import (
    mark_cow_pregnant,
    register_calf_birth,
    assign_worker_to_cow,
    sell_cow,
    mark_cow_dead,
)
# endpoint to mark cow pregnant
class MarkCowPregnantAPIView(APIView):

    def post(self, request, cow_id):

        cow = get_object_or_404(Cow, id=cow_id)

        try:
            cow = mark_cow_pregnant(cow)

        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CowSerializer(cow).data,
            status=status.HTTP_200_OK
        )
# endpoint to register calf birth


class RegisterCalfBirthAPIView(APIView):
    def post(self, request, cow_id):
        mother = get_object_or_404(Cow, id=cow_id)
        serializer = RegisterCalfBirthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            calf = register_calf_birth(
                mother=mother,
                name=serializer.validated_data["name"],
                breed=serializer.validated_data["breed"],
                sex=serializer.validated_data["sex"],
                date_of_birth=serializer.validated_data["date_of_birth"],
            )
        # 2. Update this block to catch BOTH types of exceptions cleanly
        except (DRFValidationError, DjangoValidationError) as e:
            error_message = e.detail if hasattr(e, 'detail') else e.messages
            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CalfSerializer(calf).data,
            status=status.HTTP_201_CREATED
        )

# endpoint to assign worker to cow
class AssignWorkerToCowAPIView(APIView):

    def post(self, request, cow_id):

        cow = get_object_or_404(Cow, id=cow_id)

        serializer = AssignWorkerSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        worker = get_object_or_404(
            Worker,
            id=serializer.validated_data["worker_id"]
        )

        try:
            assign_worker_to_cow(
                worker=worker,
                cow=cow
            )

        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "detail": "Worker assigned to cow successfully."
            },
            status=status.HTTP_200_OK
        )
# endpoint to sell a cow
class SellCowAPIView(APIView):

    def post(self, request, cow_id):

        cow = get_object_or_404(Cow, id=cow_id)

        try:
            cow = sell_cow(cow)

        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CowSerializer(cow).data,
            status=status.HTTP_200_OK
        )
# endpoint to mark cow deed
class MarkCowDeadAPIView(APIView):

    def post(self, request, cow_id):

        cow = get_object_or_404(Cow, id=cow_id)

        try:
            cow = mark_cow_dead(cow)

        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CowSerializer(cow).data,
            status=status.HTTP_200_OK
        )
