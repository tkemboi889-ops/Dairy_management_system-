from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from Edairy.models import Cow, Worker, Calf

User = get_user_model()


class AnimalAPITests(APITestCase):

    def setUp(self):
        # Create sample cow
        self.cow = Cow.objects.create(
            name="Bessie", breed="Friesian", sex="F", date_of_birth="2022-01-01"
        )

        # Create a user first, then create the worker linked to that user
        self.user = User.objects.create_user(
            username="johndoe", password="password123"
        )
        self.worker = Worker.objects.create(
            user=self.user, 
            phone_number="123456789"
        )

        # URLs
        self.mark_pregnant_url = reverse("Animal_management:api_pregnant", kwargs={"cow_id": self.cow.id})
        self.register_calf_url = reverse("Animal_management:api_register_birth", kwargs={"cow_id": self.cow.id})
        self.assign_worker_url = reverse("Animal_management:api_assign_worker", kwargs={"cow_id": self.cow.id})
        self.sell_cow_url = reverse("Animal_management:api_sell", kwargs={"cow_id": self.cow.id})
        self.mark_dead_url = reverse("Animal_management:api_mark_dead", kwargs={"cow_id": self.cow.id})

    # ==========================================
    # 1. Mark Cow Pregnant Tests
    # ==========================================
    def test_mark_cow_pregnant_success(self):
        response = self.client.post(self.mark_pregnant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cow.refresh_from_db()

    def test_mark_cow_pregnant_not_found(self):
        url = reverse("Animal_management:api_pregnant", kwargs={"cow_id": 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==========================================
    # 2. Register Calf Birth Tests
    # ==========================================
    def test_register_calf_birth_success(self):
       
        # 1. Mark the cow pregnant first 
        self.client.post(self.mark_pregnant_url)

        # 2. Now try registering the birth
        data = {
            "name": "Bessie Junior",
            "breed": "Friesian",
            "sex": "F",
            "date_of_birth": "2026-01-01"
        }
        response = self.client.post(self.register_calf_url, data, format="json")
        
        # You can print response.data here if it still fails, to see the exact validation error message:
        # print(response.data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Calf.objects.count(), 1)
        self.assertEqual(Calf.objects.first().name, "Bessie Junior")

    def test_register_calf_birth_invalid_data(self):
        data = {
            "breed": "Friesian",
        }
        response = self.client.post(self.register_calf_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==========================================
    # 3. Assign Worker to Cow Tests
    # ==========================================
    def test_assign_worker_to_cow_success(self):
        data = {"worker_id": self.worker.id}
        response = self.client.post(self.assign_worker_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Worker assigned to cow successfully.")

    def test_assign_worker_to_cow_invalid_worker(self):
        data = {"worker_id": 9999}
        response = self.client.post(self.assign_worker_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==========================================
    # 4. Sell Cow Tests
    # ==========================================
    def test_sell_cow_success(self):
        response = self.client.post(self.sell_cow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ==========================================
    # 5. Mark Cow Dead Tests
    # ==========================================
    def test_mark_cow_dead_success(self):
        response = self.client.post(self.mark_dead_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)