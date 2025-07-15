# create unit test
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import get_user_model
from .tokens import account_activation_token

# Create your tests here.
User = get_user_model()

class RegistrationTestCase(TestCase):
    def test_registration_sends_email(self):
        response = self.client.post(reverse('create_user'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'address': '123 Test St',
            'program': 1,  # Assuming you have programs seeded in your test db
            'middle_initial': 'T',
            'birthday': '2000-01-01',
            'department':'CICT',
            'role':'Faculty'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)  # Check that an email has been sent
        self.assertIn('Activate your account', mail.outbox[0].subject)  # Check the email subject

class ActivationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testuser@example.com', is_active=False)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activation(self):
        response = self.client.get(reverse('activate', args=[self.uid, self.token]))
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_active)