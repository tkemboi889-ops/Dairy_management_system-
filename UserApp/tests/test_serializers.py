from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from UserApp.serializers import RegistrationSerializer, LoginSerializer

User = get_user_model()

class SerializerValidationTests(TestCase):

    def setUp(self):
        """Set up an active sample profile inside our test scope."""
        self.username = "farm_admin"
        self.password = "SecurePass123!"
        self.phone = "+254711223344"
        
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            phone_number=self.phone
        )

    def test_registration_serializer_saves_securely(self):
        """Verify the registration serializer securely processes user input data."""
        data = {
            "username": "new_ranch_hand",
            "password": "WorkerPassword789!",
            "phone_number": "+254799887766"
        }
        serializer = RegistrationSerializer(data=data)
        
        # Ensure data format matches expectations
        self.assertTrue(serializer.is_valid())
        
        # Save and verify instance setup in database
        new_user = serializer.save()
        self.assertEqual(new_user.username, "new_ranch_hand")
        self.assertEqual(new_user.phone_number, "+254799887766")
        
        # CRITICAL: Verify password is encrypted and not stored as raw text
        self.assertNotEqual(new_user.password, "WorkerPassword789!")

    def test_login_serializer_with_valid_credentials(self):
        """Verify the login validation context maps the authentic profile successfully."""
        data = {
            "username": self.username,
            "password": self.password
        }
        serializer = LoginSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_login_serializer_raises_error_for_invalid_credentials(self):
        """Verify invalid passwords throw a specific Validation Error block."""
        data = {
            "username": self.username,
            "password": "WrongPasswordX"
        }
        serializer = LoginSerializer(data=data)
        
        # This should fail validation checks completely
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Invalid username or password")
