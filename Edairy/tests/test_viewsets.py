from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class EdairyViewSetTests(APITestCase):

    def setUp(self):
        """Create and force-authenticate a custom user context environment."""
        self.user = User.objects.create_user(
            username="ranch_hand",
            password="securepassword123"
        )
        # 💡 Use DRF's force_authenticate to bypass Token/JWT requirements safely
        self.client.force_authenticate(user=self.user)

    def test_get_calves_list_success(self):
        """Test retrieving calf router endpoint status."""
        url = reverse("Edairy:calf-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cows_list_success(self):
        """Test retrieving cow router endpoint status."""
        url = reverse("Edairy:cow-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workers_list_success(self):
        """Test retrieving worker router endpoint status."""
        url = reverse("Edairy:worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_feeds_list_success(self):
        """Test retrieving feed router endpoint status."""
        url = reverse("Edairy:feed-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_milk_logs_success(self):
        """Test retrieving milk router endpoint status."""
        url = reverse("Edairy:milk-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_request_fails(self):
        """Verify that dropping authentication results in a 401 Unauthorized status."""
        # 💡 To logout with force_authenticate, you pass None
        self.client.force_authenticate(user=None)
        url = reverse("Edairy:cow-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
