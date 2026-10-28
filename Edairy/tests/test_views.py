from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from Edairy.models import Calf, Cow, Worker, Feed, farm_manager, Milk

User = get_user_model()

class EdairyViewsTestCase(TestCase):

 def setUp(self):

    # --------------------------------------------------
    # 1. CREATE AUTHORIZED USER
    # --------------------------------------------------

    self.authorized_user = User.objects.create_user(
        username="auth_user",
        password="password123",
        is_staff=True
    )

    # Assign all permissions
    permissions = Permission.objects.all()
    self.authorized_user.user_permissions.set(permissions)

    # --------------------------------------------------
    # 2. CREATE UNAUTHORIZED USER
    # --------------------------------------------------

    self.unauthorized_user = User.objects.create_user(
        username="unauth_user",
        password="password123"
    )

    # --------------------------------------------------
    # 3. CREATE FARM MANAGER
    # --------------------------------------------------

    self.farm_manager = farm_manager.objects.create(
        user=self.authorized_user,
        phone_number="+254700000000"
    )

    # --------------------------------------------------
    # 4. CREATE COW
    # --------------------------------------------------

    self.cow = Cow.objects.create(
        name="Bessie",
        breed="Holstein",
        sex="F",
        date_of_birth=date(2021, 1, 1),
        status="ACTIVE",
        farm_manager=self.farm_manager
    )

    # --------------------------------------------------
    # 5. CREATE CALF
    # --------------------------------------------------

    self.calf = Calf.objects.create(
        name="Little Spot",
        breed="Holstein",
        sex="M",
        cow=self.cow
    )

    # --------------------------------------------------
    # 6. CREATE FEED
    # --------------------------------------------------

    self.feed = Feed.objects.create(
        name="Silage",
        store_number=1,
        cow=self.cow
    )

    # --------------------------------------------------
    # 7. CREATE MILK RECORD
    # --------------------------------------------------

    self.milk = Milk.objects.create(
        amount_in_litres=15.5,
        cow=self.cow
    )

    # --------------------------------------------------
    # 8. CREATE WORKER
    # --------------------------------------------------

    self.worker = Worker.objects.create(
        user=self.unauthorized_user,
        phone_number="+254711111111"
    )


# ======================================================
# CALF TESTS
# ======================================================

def test_calfs_list_view(self):

    response = self.client.get(
        reverse("Edairy:calfs_list")
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
        response,
        "edairy/calf/calf_list.html"
    )

    self.assertContains(
        response,
        "Little Spot"
    )


def test_calf_details_view(self):

    url = reverse(
        "Edairy:calf_details",
        kwargs={"pk": self.calf.pk}
    )

    response = self.client.get(url)

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
        response,
        "edairy/calf/calf_detail.html"
    )


def test_add_calf_permission_denied_for_unauthorized_user(self):

    self.client.force_login(
        self.unauthorized_user
    )

    response = self.client.get(
        reverse("Edairy:add_calf")
    )

    self.assertIn(
        response.status_code,
        [302, 403]
    )


def test_add_calf_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    payload = {
        "name": "Daisy",
        "breed": "Jersey",
        "sex": "F",
        "cow": self.cow.pk
    }

    response = self.client.post(
        reverse("Edairy:add_calf"),
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertTrue(
        Calf.objects.filter(
            name="Daisy"
        ).exists()
    )


def test_update_calf_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    url = reverse(
        "Edairy:update_calf",
        kwargs={"pk": self.calf.pk}
    )

    payload = {
        "name": "Updated Spot",
        "breed": "Holstein",
        "sex": "M",
        "cow": self.cow.pk
    }

    response = self.client.post(
        url,
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.calf.refresh_from_db()

    self.assertEqual(
        self.calf.name,
        "Updated Spot"
    )


def test_delete_calf_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    url = reverse(
        "Edairy:delete_calf",
        kwargs={"pk": self.calf.pk}
    )

    response = self.client.post(url)

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertFalse(
        Calf.objects.filter(
            pk=self.calf.pk
        ).exists()
    )


# ======================================================
# COW TESTS
# ======================================================

def test_cows_list_view(self):

    response = self.client.get(
        reverse("Edairy:cow_list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertTemplateUsed(
        response,
        "edairy/cow/cow_list.html"
    )

    self.assertContains(
        response,
        "Bessie"
    )


def test_add_cow_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    payload = {
        "name": "Molly",
        "breed": "Ayrshire",
        "sex": "F",
        "date_of_birth": "2022-01-01",
        "status": "ACTIVE",
        "farm_manager": self.farm_manager.pk
    }

    response = self.client.post(
        reverse("Edairy:add_cow"),
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertTrue(
        Cow.objects.filter(
            name="Molly"
        ).exists()
    )


def test_delete_cow_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    url = reverse(
        "Edairy:delete_cow",
        kwargs={"pk": self.cow.pk}
    )

    response = self.client.post(url)

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertFalse(
        Cow.objects.filter(
            pk=self.cow.pk
        ).exists()
    )


# ======================================================
# FEED TESTS
# ======================================================

def test_feeds_list_view(self):

    response = self.client.get(
        reverse("Edairy:feeds_list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertTemplateUsed(
        response,
        "edairy/feed/feed_list.html"
    )


def test_add_feeds_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    payload = {
        "name": "Hay",
        "store_number": 2,
        "cow": self.cow.pk
    }

    response = self.client.post(
        reverse("Edairy:add_feeds"),
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertTrue(
        Feed.objects.filter(
            name="Hay"
        ).exists()
    )


# ======================================================
# MILK TESTS
# ======================================================

def test_milk_list_view(self):

    response = self.client.get(
        reverse("Edairy:milk_list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertTemplateUsed(
        response,
        "edairy/milk/milk_list.html"
    )


def test_add_milk_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    payload = {
        "amount_in_litres": 20.0,
        "cow": self.cow.pk
    }

    response = self.client.post(
        reverse("Edairy:add_milk"),
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertTrue(
        Milk.objects.filter(
            amount_in_litres=20.0
        ).exists()
    )


# ======================================================
# WORKER TESTS
# ======================================================

def test_workers_list_view(self):

    response = self.client.get(
        reverse("Edairy:workers_list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertTemplateUsed(
        response,
        "edairy/worker/worker_list.html"
    )


def test_delete_worker_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    url = reverse(
        "Edairy:delete_worker",
        kwargs={"pk": self.worker.pk}
    )

    response = self.client.post(url)

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertFalse(
        Worker.objects.filter(
            pk=self.worker.pk
        ).exists()
    )


# ======================================================
# FARM MANAGER TESTS
# ======================================================

def test_farmers_list_view(self):

    response = self.client.get(
        reverse("Edairy:farmers_list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertTemplateUsed(
        response,
        "edairy/farmer/farmer_list.html"
    )


def test_add_farmer_view_post_success(self):

    self.client.force_login(
        self.authorized_user
    )

    new_user = User.objects.create_user(
        username="farmer2",
        password="password123"
    )

    payload = {
        "user": new_user.pk,
        "phone_number": "+254722222222"
    }

    response = self.client.post(
        reverse("Edairy:add_farmer"),
        data=payload
    )

    self.assertEqual(
        response.status_code,
        302
    )

    self.assertTrue(
        farm_manager.objects.filter(
            phone_number="+254722222222"
        ).exists()
    )

