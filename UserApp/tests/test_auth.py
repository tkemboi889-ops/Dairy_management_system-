from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthenticationAPITests(APITestCase):

    def setUp(self):
        """Set up testing variables and a default user structure."""
        self.register_url = reverse("UserApp:api_register")  
        self.login_url = reverse("UserApp:api_login")        
        self.logout_url = reverse("UserApp:api_logout")      
        
        self.username = "farm_manager"
        self.password = "SecurePassword123!"
        self.email = "manager@dairyfarm.com"
        
        # Create a pre-existing user for testing login and logout
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_registration_success(self):
        """Verify that a new user can successfully register via the API."""
        payload = {
            "username": "new_worker",
            "email": "worker@dairyfarm.com",
            "password": "AnotherSecurePassword123!",
            "confirm_password": "AnotherSecurePassword123!",
            "phone_number": "+254700000000"  # ✅ Fixed: Added required field to prevent KeyError
        }
        response = self.client.post(self.register_url, data=payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_worker").exists())

    def test_login_success_returns_token(self):
        """Verify that valid credentials return an authentication token."""
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, data=payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_logout_success(self):
        """Verify an authenticated user can log out, deleting their token."""
        token = Token.objects.create(user=self.user)
        
        # ✅ Fixed: Force the test client to pass token validation state without session interference
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
        # We explicitly force the API test client to request json format to avoid HTML page overrides
        response = self.client.post(self.logout_url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_unauthenticated_user_cannot_logout(self):
        """Verify that the Logout endpoint blocks users without a token (HTTP 401)."""
        self.client.credentials()  # Wipe out credentials
        
        # ✅ Fixed: Request json format explicitly to ensure DRF authentication error handling triggers
        response = self.client.post(self.logout_url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
