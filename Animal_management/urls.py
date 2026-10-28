from django.urls import path

from .views import (
    mark_cow_pregnant_view,
    register_calf_birth_view,
    assign_worker_to_cow_view,
    sell_cow_view,
    mark_cow_dead_view,
)
from .api_views import (
    MarkCowPregnantAPIView,
    RegisterCalfBirthAPIView,
    AssignWorkerToCowAPIView,
    SellCowAPIView,
    MarkCowDeadAPIView,
)

app_name = "Animal_management"

urlpatterns = [
    
    path("cows/<int:cow_id>/pregnant/", mark_cow_pregnant_view, name="pregnant"),
    path("cows/<int:cow_id>/register_birth/", register_calf_birth_view, name="register_birth"),
    path("cows/<int:cow_id>/assig_-worker/", assign_worker_to_cow_view, name="assign_worker"), 
    path("cows/<int:cow_id>/sell/", sell_cow_view, name="sell"),
    path("cows/<int:cow_id>/mark_dead/", mark_cow_dead_view, name="mark_dead"),
    
    # 🔌 REST API Endpoints 
    path(
        "api/cows/<int:cow_id>/pregnant/", 
        MarkCowPregnantAPIView.as_view(), 
        name="api_pregnant"
    ),
    path(
        "api/cows/<int:cow_id>/register_birth/", 
        RegisterCalfBirthAPIView.as_view(), 
        name="api_register_birth"
    ),
    path(
        "api/cows/<int:cow_id>/assign_worker/", 
        AssignWorkerToCowAPIView.as_view(), 
        name="api_assign_worker"
    ),
    path(
        "api/cows/<int:cow_id>/sell/", 
        SellCowAPIView.as_view(), 
        name="api_sell"
    ),
    path(
        "api/cows/<int:cow_id>/mark_dead/", 
        MarkCowDeadAPIView.as_view(), 
        name="api_mark_dead"
    ),
]
