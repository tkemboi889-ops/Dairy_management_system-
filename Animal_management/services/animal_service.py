from django.core.exceptions import ValidationError
from django.db import transaction

from Edairy.models import Cow, Calf, Worker


# ==========================================
# MARK COW AS PREGNANT
# ==========================================

@transaction.atomic
def mark_cow_pregnant(cow):

    # Only female cows can become pregnant
    if cow.sex != "F":
        raise ValidationError(
            "Only female cows can become pregnant."
        )

    # Dead cows cannot become pregnant
    if cow.status == "DEAD":
        raise ValidationError(
            "A dead cow cannot become pregnant."
        )

    # Sold cows cannot become pregnant
    if cow.status == "SOLD":
        raise ValidationError(
            "A sold cow cannot become pregnant."
        )

    # Prevent duplicate pregnancy registration
    if cow.status == "PREGNANT":
        raise ValidationError(
            "This cow is already pregnant."
        )

    cow.status = "PREGNANT"
    cow.save()

    return cow


# ==========================================
# REGISTER CALF BIRTH
# ==========================================

@transaction.atomic
def register_calf_birth(
    mother,
    name,
    breed,
    sex,
    date_of_birth
):

    # Ensure the animal is female
    if mother.sex != "F":
        raise ValidationError(
            "Only a female cow can give birth."
        )

    # Dead or sold cows cannot give birth
    if mother.status in ["DEAD", "SOLD"]:
        raise ValidationError(
            "Cannot register a calf for this cow."
        )

    # Cow must be pregnant
    if mother.status != "PREGNANT":
        raise ValidationError(
            "Cow must be pregnant before registering a birth."
        )

    # Create the calf
    calf = Calf.objects.create(
        cow=mother,
        name=name,
        breed=breed,
        sex=sex,
        date_of_birth=date_of_birth,
        status="ACTIVE"
    )

    # After giving birth, mother becomes active again
    mother.status = "ACTIVE"
    mother.save()

    return calf


# ==========================================
# ASSIGN WORKER TO COW



@transaction.atomic
def assign_worker_to_cow(worker, cow):
    # Lock the cow instance to prevent concurrent status updates
    cow = cow.__class__.objects.select_for_update().get(pk=cow.pk)

    # Cannot assign workers to dead cows
    if cow.status == "DEAD":
        raise ValidationError("Cannot assign a worker to a dead cow.")

    # Cannot assign workers to sold cows
    if cow.status == "SOLD":
        raise ValidationError("Cannot assign a worker to a sold cow.")

    # Check whether worker is already assigned
    if worker.cows.filter(id=cow.id).exists():
        raise ValidationError("This worker is already assigned to this cow.")

    worker.cows.add(cow)
    return worker


# ==========================================
# SELL COW
# ==========================================

@transaction.atomic
def sell_cow(cow):
    # Lock the row during status updates
    cow = cow.__class__.objects.select_for_update().get(pk=cow.pk)

    # Dead cows cannot be sold
    if cow.status == "DEAD":
        raise ValidationError("A dead cow cannot be sold.")

    # Prevent selling twice
    if cow.status == "SOLD":
        raise ValidationError("This cow has already been sold.")

    cow.status = "SOLD"
    cow.save(update_fields=["status"])
    
    # Optional clean-up: Remove worker assignments upon sale
    if hasattr(cow, "workers"):
        cow.workers.clear()

    return cow


# ==========================================
# MARK COW AS DEAD
# ==========================================

@transaction.atomic
def mark_cow_dead(cow):
    # Lock the row during status updates
    cow = cow.__class__.objects.select_for_update().get(pk=cow.pk)

    # Sold cows cannot be marked as dead
    if cow.status == "SOLD":
        raise ValidationError("A sold cow cannot be marked as dead.")

    # Prevent duplicate operation
    if cow.status == "DEAD":
        raise ValidationError("This cow is already marked as dead.")

    cow.status = "DEAD"
    cow.save(update_fields=["status"])

    # Optional clean-up: Remove worker assignments upon death
    if hasattr(cow, "workers"):
        cow.workers.clear()

    return cow