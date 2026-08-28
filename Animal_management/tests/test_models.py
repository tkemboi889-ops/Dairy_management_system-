from django.test import TestCase
from django.contrib.auth import get_user_model

from Edairy.models import Cow, Calf,farm_manager

from django.test import TestCase
from django.contrib.auth import get_user_model
# Ensure you import FarmManager, Cow, and Calf models here

User = get_user_model()


class CowModelTest(TestCase):
    def setUp(self):
        # Fix 1: Invoke get_user_model() as a function
        self.user = User.objects.create_user(
            username="manager1",
            password="TestPassword123"
        )

        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0714490438"
        )

        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_cow_is_created_successfully(self):
        self.assertEqual(self.cow.name, "Daisy")
        self.assertEqual(self.cow.breed, "Friesian")
        self.assertEqual(self.cow.sex, "F")
        self.assertEqual(self.cow.status, "ACTIVE")


class CalfModelTest(TestCase):
    def setUp(self):
        # Create user & farm_manager first so Cow validation passes
        self.user = User.objects.create_user(
            username="manager2",
            password="TestPassword123"
        )

        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0714490439"
        )

        # Fix 2: Include farm_manager when creating the mother Cow
        self.mother = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

        self.calf = Calf.objects.create(
            cow=self.mother,
            name="Junior",
            breed="Friesian",
            sex="M",
            status="ACTIVE"
        )

    def test_calf_is_linked_to_mother(self):
        self.assertEqual(self.calf.cow, self.mother)

    def test_calf_name(self):
        self.assertEqual(self.calf.name, "Junior")

