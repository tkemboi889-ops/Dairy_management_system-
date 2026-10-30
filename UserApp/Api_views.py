
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
from drf_spectacular.utils import extend_schema,inline_serializer
# Registration apiView
class RegisterAPIView(generics.CreateAPIView):
    queryset = Management.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    

#implementing django rest framework authentication
# Login apiView

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer})
    
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })
    #implementing logoutapiview
  
class LogoutView(APIView):
    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, inline_serializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = inline_serializer(
        name='LogoutResponseSerializer', 
        fields={'detail': serializers.CharField()}
    )

    @extend_schema(
        request=None,  # No request body needed for logout
        responses={
            200: inline_serializer(
                name='LogoutSuccessResponse',
                fields={
                    'detail': serializers.CharField(
                        default='Successfully logged out.'
                    )
                },
            )
        },
        description='Logs out the user by blacklisting or clearing tokens.',
    )
    def post(self, request):
        # Your actual logout logic goes here (e.g., blacklisting refresh token)
        return Response(
            {'detail': 'Successfully logged out.'}, 
            status=status.HTTP_200_OK
        )
        

