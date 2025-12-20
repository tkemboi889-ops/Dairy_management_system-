
from rest_framework import  viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import CalfSerializer,WorkerSerializer,FeedSerializer,CowSerializer,MilkSerializer,OwnerSerializer
from .models import Calf,Cow,Milk,Feed,Owner,Worker
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
    queryset=Owner.objects.all()
    serializer_class=OwnerSerializer
    permission_classes=[IsAdminUser]