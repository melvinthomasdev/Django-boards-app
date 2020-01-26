from django.test import TestCase

# Create your tests here.
from .views import signup
from django.contrib.auth.forms import UserCreationForm
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from .forms import SignUpForm



class SignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(reverse('signup'))

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_signup_url_resolves_signup_view(self):
		view=resolve('/signup/')
		self.assertEquals(view.func, signup)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 5)
		self.assertContains(self.response, 'type="text"', 1)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url=reverse('signup')
		data={
		'username':'john',
		'password1': 'abcdef123',
		'password2': 'abcdef123'
		}
		self.response = self.client.post(url,data)
		self.home_url=reverse('home')

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		response = self.client.get('home_url')
		user=self.response.context.get('user')
		self.assertTrue(user.is_authenticated)