from django.test import TestCase
from UserApp.forms import registration_form

class RegistrationFormTests(TestCase):

    def test_form_validation_with_valid_data(self):
        """Verify the form is valid when required fields are correctly completed."""
        form_data = {
            "username": "farm_supervisor",
            "phone_number": "+254711223344",
            "password1": "SecurePass123!",  # Django's internal field name
            "password2": "SecurePass123!",  # Django's internal confirmation field name
        }
        form = registration_form(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_text())

    def test_form_validation_fails_on_mismatched_passwords(self):
        """Verify the form drops errors if the password checks do not match."""
        form_data = {
            "username": "farm_worker",
            "phone_number": "+254700112233",
            "password1": "SecretPassword123",
            "password2": "DifferentPassword456",
        }
        form = registration_form(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_validation_fails_on_missing_required_fields(self):
        """Verify that omitting the username invalidates the form submission."""
        form_data = {
            "username": "",  # Blank username
            "phone_number": "+254700112233",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!"
        }
        form = registration_form(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
