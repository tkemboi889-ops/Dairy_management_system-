from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from Edairy.models import Cow, farm_manager
# Adjust the import path below if your forms file has a specific name (e.g., Edairy.forms)
from Edairy.forms import calform, cowform, milkform, workerform, feedform, farmerform

User = get_user_model()


class EdairyFormsTest(TestCase):

    def setUp(self):
        """Set up foreign key dependencies required for form validation."""
        self.user_manager = User.objects.create_user(
            username="manager1", 
            password="password123"
        )
        self.user_worker = User.objects.create_user(
            username="worker1", 
            password="password123"
        )

        self.farm_manager_instance = farm_manager.objects.create(
            user=self.user_manager,
            phone_number="+254700000000"
        )

        self.cow_instance = Cow.objects.create(
            name="Bessie",
            breed="Holstein",
            sex="F",
            date_of_birth=date(2021, 1, 1),
            status="ACTIVE",
            farm_manager=self.farm_manager_instance
        )

    
    # 1. CALFORM TESTS (Fields: name, breed)
    
    def test_calform_valid_data(self):
        """Test calform with valid name and breed."""
        data = {
            "name": "Little Spot",
            "breed": "Holstein"
        }
        form = calform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_calform_missing_required_fields(self):
        """Test calform fails when fields are missing."""
        data = {"name": "Little Spot"}  # Missing breed
        form = calform(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("breed", form.errors)

    
    # 2. COWFORM TESTS (Fields: name, breed)
    
    def test_cowform_valid_data(self):
        """Test cowform with valid name and breed."""
        data = {
            "name": "Daisy",
            "breed": "Jersey"
        }
        form = cowform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_cowform_missing_name(self):
        """Test cowform fails without a name."""
        data = {"breed": "Jersey"}
        form = cowform(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    
    # 3. MILKFORM TESTS (Fields: __all__)
    
    def test_milkform_valid_data(self):
        """Test milkform with valid amount and cow ForeignKey."""
        data = {
            "amount_in_litres": 12.5,
            "cow": self.cow_instance.pk
        }
        form = milkform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_milkform_missing_cow(self):
        """Test milkform fails without selecting a cow."""
        data = {"amount_in_litres": 15.0}
        form = milkform(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("cow", form.errors)

    
    # 4. WORKERFORM TESTS (Fields: __all__)
    
    def test_workerform_valid_data(self):
        """Test workerform with user, phone number, and cow ManyToMany."""
        data = {
            "user": self.user_worker.pk,
            "phone_number": "+254711111111",
            "cows": [self.cow_instance.pk]
        }
        form = workerform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    
    # 5. FEEDFORM TESTS (Fields: __all__)
    
    def test_feedform_valid_data(self):
        """Test feedform with name, store_number, and cow ForeignKey."""
        data = {
            "name": "Silage",
            "store_number": 101,
            "cow": self.cow_instance.pk
        }
        form = feedform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    
    # 6. FARMERFORM TESTS (Fields: __all__)
    
    def test_farmerform_valid_data(self):
        """Test farmerform with user and phone number."""
        new_user = User.objects.create_user(
            username="new_manager", 
            password="password123"
        )
        data = {
            "user": new_user.pk,
            "phone_number": "+254722222222"
        }
        form = farmerform(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)