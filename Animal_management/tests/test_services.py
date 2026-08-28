
# test making a cow pregnant
from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from Animal_management.models import Cow
from Edairy.models import farm_manager
from Animal_management.services.animal_service import (
    mark_cow_pregnant,
    register_calf_birth,
    sell_cow,
    mark_cow_dead,
)
User = get_user_model()

class MarkCowPregnantServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="pregnant_service_manager",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0700000001"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_female_cow_can_be_marked_pregnant(self):
        mark_cow_pregnant(self.cow)
        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "PREGNANT")

    def test_male_cow_cannot_be_marked_pregnant(self):
        male_cow = Cow.objects.create(
            name="Bull",
            breed="Friesian",
            sex="M",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )
        with self.assertRaises(ValidationError):
            mark_cow_pregnant(male_cow)

    def test_dead_cow_cannot_become_pregnant(self):
        dead_cow = Cow.objects.create(
            name="Dead Cow",
            breed="Friesian",
            sex="F",
            status="DEAD",
            farm_manager=self.farm_manager
        )
        with self.assertRaises(ValidationError):
            mark_cow_pregnant(dead_cow)


class RegisterCalfBirthServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="birth_service_manager",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0700000002"
        )
        self.mother = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="PREGNANT",
            farm_manager=self.farm_manager
        )

    def test_register_calf_birth(self):
        calf = register_calf_birth(
            mother=self.mother,
            name="Junior",
            breed="Friesian",
            sex="M",
            date_of_birth=date.today()
        )
        self.assertIsInstance(calf)
        self.assertEqual(calf.name, "Junior")
        self.assertEqual(calf.cow, self.mother)

        self.mother.refresh_from_db()
        self.assertEqual(self.mother.status, "ACTIVE")

    def test_non_pregnant_cow_cannot_register_birth(self):
        cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )
        with self.assertRaises(ValidationError):
            register_calf_birth(
                mother=cow,
                name="Junior",
                breed="Friesian",
                sex="M",
                date_of_birth=date.today()
            )


class SellCowServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="sell_service_manager",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0700000003"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_sell_cow(self):
        sell_cow(self.cow)
        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "SOLD")

    def test_dead_cow_cannot_be_sold(self):
        self.cow.status = "DEAD"
        self.cow.save()
        with self.assertRaises(ValidationError):
            sell_cow(self.cow)


class MarkCowDeadServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="dead_service_manager",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0700000004"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_mark_cow_dead(self):
        mark_cow_dead(self.cow)
        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "DEAD")

    def test_sold_cow_cannot_be_marked_dead(self):
        self.cow.status = "SOLD"
        self.cow.save()
        with self.assertRaises(ValidationError):
            mark_cow_dead(self.cow)





