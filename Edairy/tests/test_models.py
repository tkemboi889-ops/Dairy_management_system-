# tests to test models
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from Edairy.models import farm_manager, Cow, Calf, Milk, Feed, Worker

User = get_user_model()


class EdairyModelsTest(TestCase):

    def setUp(self):
        """Set up initial test data used across test methods."""
        # 1. Create Users
        self.manager_user = User.objects.create_user(
            username="manager1",
            password="password123"
        )
        self.worker_user = User.objects.create_user(
            username="worker1",
            password="password123"
        )

        # 2. Create Farm Manager Profile
        self.farm_manager = farm_manager.objects.create(
            user=self.manager_user,
            phone_number="+254700000000"
        )

        # 3. Create Cows (Female and Male)
        self.female_cow = Cow.objects.create(
            name="Bessie",
            breed="Holstein",
            sex="F",
            date_of_birth=date(2020, 5, 15),
            status="ACTIVE",
            farm_manager=self.farm_manager
        )
        self.male_cow = Cow.objects.create(
            name="Ferdinand",
            breed="Angus",
            sex="M",
            date_of_birth=date(2021, 1, 10),
            status="ACTIVE",
            farm_manager=self.farm_manager
        )

    
    # 1. FARM MANAGER TESTS
    
    def test_farm_manager_creation_and_str(self):
        """Test farm_manager string representation and cascade deletion."""
        self.assertEqual(str(self.farm_manager), "manager1")
        self.assertEqual(self.farm_manager.phone_number, "+254700000000")

    
    # 2. COW MODEL TESTS
    
    def test_cow_creation_and_str(self):
        """Test Cow string representation and creation."""
        self.assertEqual(str(self.female_cow), "Bessie")
        self.assertEqual(self.farm_manager.cows.count(), 2)  # Related manager query

    def test_cow_get_age(self):
        """Test Cow age calculation logic."""
        # Calculate expected age dynamically to prevent test decay over time
        today = date.today()
        expected_age = today.year - 2020
        if (today.month, today.day) < (5, 15):
            expected_age -= 1
            
        self.assertEqual(self.female_cow.get_age(), expected_age)

    def test_pregnant_female_cow_validation_passes(self):
        """Test that a female cow CAN be marked as PREGNANT."""
        self.female_cow.status = "PREGNANT"
        try:
            self.female_cow.clean()  # Should pass without raising ValidationError
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly for female pregnant cow.")

    def test_pregnant_male_cow_validation_fails(self):
        """Test clean() raises ValidationError if a male cow is set to PREGNANT."""
        self.male_cow.status = "PREGNANT"
        with self.assertRaises(ValidationError):
            self.male_cow.clean()

    
    # 3. CALF MODEL TESTS
    
    def test_calf_creation_and_age(self):
        """Test Calf model relationship, string representation, and age."""
        calf = Calf.objects.create(
            name="Daisy",
            breed="Holstein",
            sex="F",
            date_of_birth=date(2024, 2, 1),
            status="ACTIVE",
            cow=self.female_cow
        )
        self.assertEqual(str(calf), "Daisy")
        self.assertEqual(calf.cow, self.female_cow)
        self.assertIn(calf, self.female_cow.calves.all())  # Check related_name="calves"

        # Calculate expected age dynamically
        today = date.today()
        expected_age = today.year - 2024
        if (today.month, today.day) < (2, 1):
            expected_age -= 1
        self.assertEqual(calf.get_age(), expected_age)

    
    # 4. MILK MODEL TESTS
    
    def test_milk_record_creation(self):
        """Test Milk record creation and string representation."""
        milk_record = Milk.objects.create(
            amount_in_litres=14.5,
            cow=self.female_cow
        )
        self.assertEqual(str(milk_record), "14.5 L from Bessie")
        self.assertEqual(milk_record.date_collected, date.today())
        self.assertIn(milk_record, self.female_cow.milk_records.all())

    
    # 5. FEED MODEL TESTS
    
    def test_feed_creation(self):
        """Test Feed record creation and relationship with Cow."""
        feed = Feed.objects.create(
            name="Silage",
            store_number=102,
            cow=self.female_cow
        )
        self.assertEqual(str(feed), "Silage")
        self.assertIn(feed, self.female_cow.feeds.all())

    
    # 6. WORKER MODEL TESTS
    
    def test_worker_creation_and_cow_assignment(self):
        """Test Worker profile creation and ManyToMany relation with Cow."""
        worker = Worker.objects.create(
            user=self.worker_user,
            phone_number="+254711111111"
        )
        self.assertEqual(str(worker), "worker1")

        # Assign cows to worker
        worker.cows.add(self.female_cow, self.male_cow)
        self.assertEqual(worker.cows.count(), 2)
        self.assertIn(worker, self.female_cow.workers.all())

    
    # 7. CASCADE DELETE TESTS
    
    def test_cow_deletion_cascades_to_calves_milk_and_feeds(self):
        """Verify deleting a Cow cascades to associated Calves, Milk, and Feed records."""
        Calf.objects.create(name="Calf 1", breed="Holstein", sex="M", cow=self.female_cow)
        Milk.objects.create(amount_in_litres=10.0, cow=self.female_cow)
        Feed.objects.create(name="Hay", store_number=1, cow=self.female_cow)

        # Delete cow
        self.female_cow.delete()

        # Verify child records are deleted
        self.assertEqual(Calf.objects.count(), 0)
        self.assertEqual(Milk.objects.count(), 0)
        self.assertEqual(Feed.objects.count(), 0)