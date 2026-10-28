import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from Edairy.models import Calf, Cow, Milk, Feed, farm_manager, Worker

class DairyManagementSystemTests(APITestCase):

    def setUp(self):
        """Set up test users and sample data before each test execution."""
        User = get_user_model()
        
        # 1. Create standard and admin users using your custom User model
        self.regular_user = User.objects.create_user(
            username='worker1', 
            password='password123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin1', 
            password='adminpassword'
        )

        # 2. Create a dummy cow instance matching your exact fields
        self.sample_cow = Cow.objects.create(
            name="Daisy",
            breed="Holstein",
            sex="F",
            date_of_birth=datetime.date(2024, 5, 12),
            status="ACTIVE"
        )

        # 3. Generate namespaced URLs matching your DefaultRouter setup
        self.cow_list_url = reverse('Edairy:cow-list')
        self.cow_detail_url = reverse('Edairy:cow-detail', kwargs={'pk': self.sample_cow.pk})
        self.farm_manager_list_url = reverse('Edairy:farm_manager-list') 

    # --- PERMISSION TESTS ---
    def test_cow_list_unauthenticated_fails(self):
        """Ensure unauthenticated users cannot access IsAuthenticated endpoints."""
        response = self.client.get(self.cow_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_farm_manager_list_regular_user_fails(self):
        """Ensure non-admin users cannot access IsAdminUser farm manager endpoints."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.farm_manager_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_farm_manager_list_admin_user_succeeds(self):
        """Ensure admin users can successfully access IsAdminUser farm manager endpoints."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.farm_manager_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- CRUD FUNCTIONALITY TESTS ---
    def test_get_cow_list_authenticated(self):
        """Ensure authorized users can fetch lists of cows."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.cow_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_cow_authenticated(self):
        """Verify POST requests successfully create new cow records."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            "name": "Bessie",
            "breed": "Jersey",
            "sex": "F",
            "date_of_birth": "2025-01-10",
            "status": "PREGNANT"
        }
        response = self.client.post(self.cow_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cow.objects.count(), 2)
