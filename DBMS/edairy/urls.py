from .views import CalfViewSet,MilkViewSet,CowViewSet,FeedViewSet,OwnerViewSet,WorkerViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'calves', CalfViewSet, basename='calf')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'feeds', FeedViewSet, basename='feed')
router.register(r'cows', CowViewSet, basename='cow')
router.register(r'milk', MilkViewSet, basename='milk')
router.register(r'owners', OwnerViewSet, basename='owner')

urlpatterns=[
    path('',include(router.urls)),
]