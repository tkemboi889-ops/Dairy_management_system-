from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

class ManagementModelTests(TestCase):

    def test_create_user_success(self):
        """Verify standard user creation applies inputs and password hashing correctly."""
        username = "dairy_worker1"
        password = "SecureWorkerPassword123!"
        phone = "+254711223344"
        
        user = User.objects.create_user(
            username=username,
            password=password,
            phone_number=phone
        )
        
        self.assertEqual(user.username, username)
        self.assertEqual(user.phone_number, phone)
        # Verify base properties are appropriately assigned
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # CRITICAL: Verify the password is encrypted, not saved in plain text
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))

    def test_create_user_raises_value_error_if_no_username(self):
        """Verify that omitting a username drops a clear, expected ValueError."""
        with self.assertRaisesMessage(ValueError, "Username is required."):
            User.objects.create_user(
                username="",
                password="SomePassword123",
                phone_number="+254700000000"
            )

    def test_create_superuser_success(self):
        """Verify that superuser initialization automatically enforces required access permissions."""
        username = "farm_owner"
        password = "AdminSecurePassword987!"
        
        superuser = User.objects.create_superuser(
            username=username,
            password=password
        )
        
        self.assertEqual(superuser.username, username)
        # Superusers must have elevated system flags active
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))

    def test_create_superuser_validation_flags(self):
        """Verify that a superuser registration fails if administrative flags are falsified."""
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                username="faulty_admin",
                password="Password123",
                is_staff=False
            )
            
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(
                username="faulty_admin2",
                password="Password123",
                is_superuser=False
            )

    def test_phone_number_uniqueness_constraint(self):
        """Verify the database schema configuration correctly blocks duplicate phone entries."""
        shared_phone = "+254722000000"
        
        # Save our primary user profile
        User.objects.create_user(username="user_one", password="Pass1", phone_number=shared_phone)
        
        # Trying to register a second account with the exact same phone number must raise an IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="user_two", password="Pass2", phone_number=shared_phone)

    def test_model_string_representation(self):
        """Verify the object's string representation returns the plain text username value."""
        user = User.objects.create_user(username="test_string_user", password="Password123")
        self.assertEqual(str(user), "test_string_user")
