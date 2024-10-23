from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

class UserViewsTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'securepassword123',
            'full_Name': 'Test User',
            'cpf': '12345678901',
            'phone_number': '+5511912345678',
            'street': 'Test Street',
            'home_number': '123',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Brazil',
        }

    def test_register_user(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(email=self.user_data['email']).exists())

    def test_login_user(self):
        # First, register the user
        self.client.post(reverse('register'), self.user_data)

        # Then try logging in
        response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

        # Get the messages and check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Login successful!', [str(message) for message in messages])

    def test_logout_user(self):
        # Register and log in the user
        self.client.post(reverse('register'), self.user_data)
        self.client.login(username=self.user_data['email'], password=self.user_data['password'])

        response = self.client.get(reverse('logout'))  # Change to 'logout'
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

        # Get the messages and check the logout message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Você foi desconectado!', [str(message) for message in messages])



    def test_register_with_invalid_data(self):
        # Test registration with missing fields
        invalid_data = self.user_data.copy()
        invalid_data['email'] = ''  # Make email empty
        
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the registration page
        self.assertContains(response, 'Por favor preencha todos os campos obrigatórios.')

    def test_login_with_invalid_credentials(self):
        self.client.post(reverse('register'), self.user_data)
        response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': 'wrongpassword',  # Incorrect password
        })
        self.assertEqual(response.status_code, 200)  # Should render the login page
        self.assertContains(response, 'Invalid email or password.')  # Adjust this message as needed

    """ def test_duplicate_registration(self):
        self.client.post(reverse('register'), self.user_data)  # First registration
        response = self.client.post(reverse('register'), self.user_data)  # Try to register again
        self.assertEqual(response.status_code, 200)  # Should stay on the registration page
        self.assertContains(response, 'A user with that email already exists.')  # Adjust this message as needed

    def test_access_protected_view_without_login(self):
        response = self.client.get(reverse('menu'))  # Replace 'menu' with a protected view
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, reverse('login'))  # Ensure it's redirecting to the login page """

    def test_successful_logout_message(self):
        self.client.post(reverse('register'), self.user_data)
        self.client.login(username=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('logout'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Você foi desconectado!', [str(message) for message in messages])