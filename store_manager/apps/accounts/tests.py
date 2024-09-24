from django.test import TestCase
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'full_name': 'John Doe',
            'cpf': '12345678900',
            'address': 'Main Street',
            'cep': '01001000',
            'street': 'Main Street',
            'street_number': '100',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brazil',
            'email': 'johndoe@example.com',
            'phone_number': '11999999999',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_cep(self):
        form_data = {
            'full_name': 'John Doe',
            'cpf': '12345678900',
            'cep': '99999999',  # Invalid CEP
            'street': '',
            'street_number': '100',
            'city': '',
            'state': '',
            'country': '',
            'email': 'johndoe@example.com',
            'phone_number': '11999999999',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cep', form.errors)

    def test_password_mismatch(self):
        form_data = {
            'full_name': 'John Doe',
            'cpf': '12345678900',
            'cep': '01001000',
            'street': 'Main Street',
            'street_number': '100',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brazil',
            'email': 'johndoe@example.com',
            'phone_number': '11999999999',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)