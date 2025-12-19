# Create your views here.
from .models import Management
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Registration View
class RegisterAPIView(generics.CreateAPIView):
    queryset = Management.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

# Login View

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        token = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })
    #implementing logout
  
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

