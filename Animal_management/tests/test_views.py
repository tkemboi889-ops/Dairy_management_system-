from django.test import TestCase
from django.urls import reverse

from Edairy.models import Cow
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Edairy.models import Cow, farm_manager

User = get_user_model()


class MarkCowPregnantViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="manager_pregnant",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0711111111"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_mark_cow_pregnant_view(self):
        url = reverse(
            "mark_cow_pregnant",
            kwargs={"cow_id": self.cow.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "PREGNANT")

    def test_get_request_is_not_allowed(self):
        url = reverse(
            "mark_cow_pregnant",
            kwargs={"cow_id": self.cow.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)


class SellCowViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="manager_sell",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0722222222"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_sell_cow_view(self):
        url = reverse(
            "sell_cow",
            kwargs={"cow_id": self.cow.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "SOLD")


class MarkCowDeadViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="manager_dead",
            password="TestPassword123"
        )
        self.farm_manager = farm_manager.objects.create(
            user=self.user,
            phone_number="0733333333"
        )
        self.cow = Cow.objects.create(
            name="Daisy",
            breed="Friesian",
            sex="F",
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    def test_mark_cow_dead_view(self):
        url = reverse(
            "mark_cow_dead",
            kwargs={"cow_id": self.cow.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.cow.refresh_from_db()
        self.assertEqual(self.cow.status, "DEAD")