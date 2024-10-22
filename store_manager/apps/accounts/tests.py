# myapp/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserTestCase(TestCase):
    
    def setUp(self):
        # This method will run before each test
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'full_Name': 'Test User',
            'cpf': '12345678901',  # Replace with a valid CPF for tests
            'phone_number': '+5511999999999',  # Replace with a valid phone number for tests
            'street': 'Test Street',
            'home_number': '123',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Brazil',
        }

    def test_create_user(self):
        user = CustomUser(**self.valid_data)
        user.set_password('password123')  # Set the password
        user.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_cpf_unique_constraint(self):
        CustomUser.objects.create(**self.valid_data)  # Create first user
        with self.assertRaises(ValidationError):
            duplicate_user = CustomUser(**self.valid_data)  # Attempt to create a user with the same CPF
            duplicate_user.clean_fields()  # This will raise the ValidationError

    def test_invalid_cpf(self):
        invalid_data = self.valid_data.copy()
        invalid_data['cpf'] = 'invalid_cpf'  # Set an invalid CPF
        user = CustomUser(**invalid_data)
        with self.assertRaises(ValidationError):
            user.clean_fields()  # Validate the user, which should raise ValidationError

    def test_phone_number_validation(self):
        # Test valid phone number
        user = CustomUser(**self.valid_data)
        user.phone_number = 'invalid_phone'
        with self.assertRaises(ValidationError):
            user.clean_fields()  # Validate the user, which should raise ValidationError

    def test_get_full_name(self):
        user = CustomUser(**self.valid_data)
        user.set_password('password123')  # Set the password
        user.save()
        self.assertEqual(user.get_full_name(), 'Test User')

