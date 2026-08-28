from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

from Edairy.models import Cow, Worker

from .services.animal_service import (
    mark_cow_pregnant,
    register_calf_birth,
    assign_worker_to_cow,
    sell_cow,
    mark_cow_dead,
)


# ==========================================
# MARK COW AS PREGNANT
# ==========================================

@require_POST
def mark_cow_pregnant_view(request, cow_id):

    cow = get_object_or_404(Cow, id=cow_id)

    try:

        mark_cow_pregnant(cow)

        messages.success(
            request,
            f"{cow.name} has been marked as pregnant."
        )

    except ValidationError as e:

        messages.error(
            request,
            e.message
        )

    return redirect("cow_list")


# ==========================================
# REGISTER CALF BIRTH
# ==========================================

def register_calf_birth_view(request, cow_id):

    mother = get_object_or_404(
        Cow,
        id=cow_id
    )

    if request.method == "POST":

        name = request.POST.get("name")
        breed = request.POST.get("breed")
        sex = request.POST.get("sex")
        date_of_birth = request.POST.get("date_of_birth")

        try:

            calf = register_calf_birth(
                mother=mother,
                name=name,
                breed=breed,
                sex=sex,
                date_of_birth=date_of_birth
            )

            messages.success(
                request,
                f"Calf {calf.name} was registered successfully."
            )

            return redirect(
                "cow_detail",
                cow_id=mother.id
            )

        except ValidationError as e:

            messages.error(
                request,
                e.message
            )

    return render(
        request,
        "animal_management/register_calf_birth.html",
        {
            "mother": mother
        }
    )



# ASSIGN WORKER TO COW


def assign_worker_to_cow_view(request, cow_id):

    cow = get_object_or_404(
        Cow,
        id=cow_id
    )

    workers = Worker.objects.all()

    if request.method == "POST":

        worker_id = request.POST.get("worker")

        worker = get_object_or_404(
            Worker,
            id=worker_id
        )

        try:

            assign_worker_to_cow(
                worker=worker,
                cow=cow
            )

            messages.success(
                request,
                f"{worker} has been assigned to {cow.name}."
            )

            return redirect(
                "cow_detail",
                cow_id=cow.id
            )

        except ValidationError as e:

            messages.error(
                request,
                e.message
            )

    return render(
        request,
        "animal_management/assign_worker.html",
        {
            "cow": cow,
            "workers": workers
        }
    )


# SELL COW

@require_POST
def sell_cow_view(request, cow_id):

    cow = get_object_or_404(
        Cow,
        id=cow_id
    )

    try:

        sell_cow(cow)

        messages.success(
            request,
            f"{cow.name} has been marked as SOLD."
        )

    except ValidationError as e:

        messages.error(
            request,
            e.message
        )

    return redirect("cow_list")


# MARK COW AS DEAD

@require_POST
def mark_cow_dead_view(request, cow_id):

    cow = get_object_or_404(
        Cow,
        id=cow_id
    )

    try:

        mark_cow_dead(cow)

        messages.success(
            request,
            f"{cow.name} has been marked as DEAD."
        )

    except ValidationError as e:

        messages.error(
            request,
            e.message
        )

    return redirect("cow_list")
