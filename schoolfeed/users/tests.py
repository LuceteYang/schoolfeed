from django.test import TestCase
from schoolfeed.users.models import User
from django.urls import reverse, resolve
from rest_framework.test import APIClient
import json

from rest_framework import status

class UsersTestMixin(TestCase):

	def setUp(self):
		self.client = APIClient()

		url = reverse('registration:rest_register')
		registrationResp = self.client.post(url, {'username':'sanghwan','email':'jae6120@naver.com','password2':'chevyspassword', 'password1':'chevyspassword','name':'박상환'})
		self.assertEqual(registrationResp.status_code, status.HTTP_201_CREATED)


		url = reverse('rest_framework:rest_login')
		resp = self.client.post(url, {'username':'sanghwan', 'password':'chevyspassword'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('token' in resp.data)
		token = resp.data['token']
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

	def test_get_users(self):
		resp = self.client.get('/api/users/', format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content.decode('utf-8'))
		self.assertTrue('profile_image' in parseResponse)
		self.assertTrue('name' in parseResponse)
		self.assertTrue('email' in parseResponse)

	def test_put_users(self):
		resp = self.client.get('/api/users/', format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content.decode('utf-8'))
		self.assertEqual(parseResponse['name'],'박상환')

		resp = self.client.put('/api/users/', {'name':'sanghwan'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content.decode('utf-8'))
		self.assertEqual('sanghwan',parseResponse['name'])

	def test_get_user_schools(self):
		resp = self.client.get('/api/users/schools/?page=1', format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content.decode('utf-8'))
		self.assertEqual(len(parseResponse),0)

	def test_get_user_contents(self):
		resp = self.client.get('/api/users/contents/?last_contents_id=0', format='json')		
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content.decode('utf-8'))
		self.assertEqual(len(parseResponse),0)