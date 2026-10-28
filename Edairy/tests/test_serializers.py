import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from Edairy.models import farm_manager, Cow, Milk, Feed
from Edairy.serializers import (
    farm_managerSerializer, WorkerSerializer, CowSerializer, 
    CalfSerializer, MilkSerializer, FeedSerializer
)

User = get_user_model()

class SerializerValidationTests(TestCase):

    def setUp(self):
        """Set up initial user accounts and model relationships."""
        # 1. Create a true user instance to attach to our base farm_manager record
        self.user1 = User.objects.create_user(
            username="manager1",
            email="duplicate@farm.com",
            password="password123"
        )
        
        # 2. Create the base farm manager record correctly using the user instance
        self.existing_manager = farm_manager.objects.create(
            user=self.user1,
            phone_number="0712345678"
        )
        
        # 3. Create a secondary user instance to evaluate validation isolation paths
        self.user2 = User.objects.create_user(
            username="manager2",
            email="unique@farm.com",
            password="password123"
        )

        self.sample_cow = Cow.objects.create(
            name="Daisy",
            breed="Holstein",
            sex="F",
            status="ACTIVE"
        )

    # --- FARM MANAGER SERIALIZER TESTS ---
    def test_farm_manager_valid_data(self):
        """Valid farm manager payload should pass validation."""
        data = {
            "user": self.user2.id, 
            "email": "alice@farm.com", 
            "phone_number": "0799887766"
        }
        serializer = farm_managerSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_farm_manager_duplicate_email_fails(self):
        """Serializer should catch duplicate emails across distinct instances."""
        data = {
            "user": self.user2.id, 
            "email": "duplicate@farm.com", 
            "phone_number": "0711111111"
        }
        serializer = farm_managerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_farm_manager_invalid_phone_fails(self):
        """Phone numbers with letters or length != 10 must fail."""
        data_letters = {
            "user": self.user2.id, 
            "email": "bob@farm.com", 
            "phone_number": "0712345abc"
        }
        data_short = {
            "user": self.user2.id, 
            "email": "bob@farm.com", 
            "phone_number": "123"
        }
        
        serializer1 = farm_managerSerializer(data=data_letters)
        serializer2 = farm_managerSerializer(data=data_short)
        
        self.assertFalse(serializer1.is_valid())
        self.assertFalse(serializer2.is_valid())

    # --- WORKER SERIALIZER TESTS ---
    def test_worker_phone_length_validation(self):
        """Worker phone number must be exactly 10 characters long."""
        invalid_data = {"name": "Sam", "phone_number": "12345"}
        serializer = WorkerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)



    # --- MILK SERIALIZER TESTS ---
        # Inside Edairy/tests/test_serializers.py

    def test_milk_future_date_fails(self):
        """Milk entries dated in the future must trigger validation errors."""
        import datetime
        future_date = datetime.date.today() + datetime.timedelta(days=2)
        
        data = {
            "cow": self.sample_cow.id, 
            "amount_in_litres": 12.5,  
            "date_collected": str(future_date)
        }
        
        
        serializer = MilkSerializer(data=data)
        serializer.fields['date_collected'].read_only = False 
        
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_collected", serializer.errors)


    # --- FEED SERIALIZER TESTS ---
    def test_feed_store_number_positive(self):
        """Store numbers must strictly resolve to integers greater than zero."""
        data = {"feed_name": "Hay", "store_number": 0}
        serializer = FeedSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("store_number", serializer.errors)
