from .Api_views import CalfViewSet,MilkViewSet,CowViewSet,FeedViewSet,OwnerViewSet,WorkerViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views  import calf_details,calfs_list,delete_calf,update_calfs,AddCalfView,add_cow,cows_list,update_cows,cow_details,delete_cow,add_feeds,feeds_list,feeds_update,feed_details,delete_feeds,add_workers,workers_list,update_workers,worker_details,delete_worker,add_farmer,farmers_list,farmers_update,farmers_detail,delete_farmer,add_milk,milk_list,update_milk,milk_details,delete_milk

router = DefaultRouter()

router.register(r'calves', CalfViewSet, basename='calf')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'feeds', FeedViewSet, basename='feed')
router.register(r'cows', CowViewSet, basename='cow')
router.register(r'milk', MilkViewSet, basename='milk')
router.register(r'owners', OwnerViewSet, basename='owner')

urlpatterns=[
    path('',include(router.urls)),
    path("calf_details/<int:pk>/", calf_details.as_view(),name="calf_details"),
    path("calf_list/",calfs_list.as_view(),name="calfs_list"),
    path("delete_calf/<int:pk>/",delete_calf.as_view(),name="delete_calf"),
    path("update_calf/<int:pk>/", update_calfs.as_view(),name="update_calfs"),
    path("add_calfs/",AddCalfView.as_view(),name="add_calf"),
    path("add_cow/",add_cow.as_view(),name="add_cow"),
    path("cow_list/",cows_list.as_view(),name="cow_list"),
    path("update_cows/<int:pk>/",update_cows.as_view(),name="update_cows"),
    path("cow_details/<int:pk>/",cow_details.as_view(),name="cow_details"),
    path("delete_cow/<int:pk>/",delete_cow.as_view(),name="delete_cow"),
    path("add_feeds/",add_feeds.as_view(),name="add_feeds"),
    path("feeds_list/",feeds_list.as_view(),name="feeds_list"),
    path("feed_updates/<int:pk>/", feeds_update.as_view(),name="feeds_update"),
    path("feed_details/<int:pk>/",feed_details.as_view(),name="feed_details"),
    path("delete_feeds/<int:pk>/",delete_feeds.as_view(),name="delete_feeds"),
    path("add_workers/", add_workers.as_view(),name="add_workers"),
    path("workers_list/",workers_list.as_view(),name="workers_list"),
    path("update_workers/<int:pk>/",update_workers.as_view(),name="update_workers"),
    path("workers_details/<int:pk>/",worker_details.as_view(),name="workers_details"),
    path("delete_worker/<int:pk>/",delete_worker.as_view(),name="delete_worker"),
    path("add_farmer/",add_farmer.as_view(),name="add_farmer"),
    path("farmers_list/",farmers_list.as_view(),name="farmers_list"),
    path("farmers_update/<int:pk>/",farmers_update.as_view(),name="farmers_update"),
    path("farmers_detail/<int:pk>/",farmers_detail.as_view(),name="farmers_details"),
    path("delete_farmer/<int:pk>/",delete_farmer.as_view(),name="delete_farmer"),
    path("add_milk/",add_milk.as_view(),name="add_milk"),
    path("milk_list/",milk_list.as_view(),name="milk_list"),
    path("update_milk/<int:pk>/",update_milk.as_view(),name="update_milk"),
    path("milk_details/<int:pk>/",milk_details.as_view(),name="milk_details"),
    path("delete_milk/<int:pk>/",delete_milk.as_view(),name="delete_milk"),
]