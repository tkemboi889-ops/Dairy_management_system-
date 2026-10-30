from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

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
    serializer_class = CowSerializer  # Satisfies basic DRF-spectacular fallback

    @extend_schema(
        request=None,  # No request body needed
        responses={200: CowSerializer},
        description="Marks a specific cow as pregnant and returns updated cow details."
    )
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
    serializer_class = RegisterCalfBirthSerializer

    @extend_schema(
        request=RegisterCalfBirthSerializer,
        responses={201: CalfSerializer},
        description="Registers a new calf birth for the specified mother cow."
    )
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
    serializer_class = AssignWorkerSerializer

    @extend_schema(
        request=AssignWorkerSerializer,
        responses={
            200: inline_serializer(
                name='WorkerAssignedResponse',
                fields={'detail': serializers.CharField()}
            )
        },
        description="Assigns a worker to a specific cow."
    )
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
    serializer_class = CowSerializer

    @extend_schema(
        request=None,
        responses={200: CowSerializer},
        description="Marks a cow as sold and returns updated cow details."
    )
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


# endpoint to mark cow dead
class MarkCowDeadAPIView(APIView):
    serializer_class = CowSerializer

    @extend_schema(
        request=None,
        responses={200: CowSerializer},
        description="Marks a cow as dead and returns updated cow details."
    )
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