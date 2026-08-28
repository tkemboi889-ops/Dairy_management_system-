from django.urls import path

from .views import (
    mark_cow_pregnant_view,
    register_calf_birth_view,
    assign_worker_to_cow_view,
    sell_cow_view,
    mark_cow_dead_view,
)


urlpatterns = [

    path(
        "cows/<int:cow_id>/pregnant/",
        mark_cow_pregnant_view,
        name="mark_cow_pregnant"
    ),

    path(
        "cows/<int:cow_id>/register-birth/",
        register_calf_birth_view,
        name="register_calf_birth"
    ),

    path(
        "cows/<int:cow_id>/assign-worker/",
        assign_worker_to_cow_view,
        name="assign_worker_to_cow"
    ),

    path(
        "cows/<int:cow_id>/sell/",
        sell_cow_view,
        name="sell_cow"
    ),

    path(
        "cows/<int:cow_id>/mark-dead/",
        mark_cow_dead_view,
        name="mark_cow_dead"
    ),
]