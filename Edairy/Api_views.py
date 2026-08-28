

# Create your views here.

from rest_framework import  viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import CalfSerializer,WorkerSerializer,FeedSerializer,CowSerializer,MilkSerializer,OwnerSerializer
from .models import Calf,Cow,Milk,Feed,farm_manager,Worker
#creating a homepage function
from django.http import JsonResponse
def home(request):
    return JsonResponse(request,{
        "message": "Dairy Management System API is running successfully ",
        "status": "OK"
    })


# Create your views here.
class CalfViewSet(viewsets.ModelViewSet):
    queryset=Calf.objects.all()
    serializer_class=CalfSerializer
    permission_classes=[IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset=Worker.objects.all()
    serializer_class=WorkerSerializer
    permission_classes=[IsAuthenticated]

class FeedViewSet(viewsets.ModelViewSet):
    queryset=Feed.objects.all()
    serializer_class=FeedSerializer
    permission_classes=[IsAuthenticated]

class CowViewSet(viewsets.ModelViewSet):
    queryset=Cow.objects.all()
    serializer_class=CowSerializer
    permission_classes=[IsAuthenticated]

class MilkViewSet(viewsets.ModelViewSet):
    queryset=Milk.objects.all()
    serializer_class=MilkSerializer
    permission_classes=[IsAuthenticated]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset=farm_manager.objects.all()
    serializer_class=OwnerSerializer
    permission_classes=[IsAdminUser]