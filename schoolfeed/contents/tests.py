from django.test import TestCase
from schoolfeed.users.models import User
from schoolfeed.contents.models import Contents
from schoolfeed.schools.models import School, Member
from django.urls import reverse, resolve
from rest_framework.test import APIClient
import json

from rest_framework import status

class ContentsTestMixin(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(email='chevy@chase.com', username='sanghwan', password='chevyspassword', name='박상환')

		url = reverse('rest_framework:rest_login')
		resp = self.client.post(url, {'username':'sanghwan', 'password':'chevyspassword'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('token' in resp.data)
		token = resp.data['token']
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
		self.school = School.objects.create(name='금호고등학교', location='광주광역시 북구 금호로 100', creator=self.user)
		Member.objects.create(school=self.school, member=self.user, role=1)
		self.contents = Contents.objects.create(school=self.school, creator=self.user, text='초기 컨텐츠입니다.')
	
	def test_create_contents(self):
		resp = self.client.post('/api/contents/',{'school':self.school.id,'text':'테스트 컨텐츠입니다.'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('id' in resp.data)
		self.assertTrue('creator' in resp.data)
		self.assertTrue('main_image' in resp.data)
		self.assertTrue('text' in resp.data)
		self.assertTrue('school' in resp.data)
		self.assertEqual(resp.data.get('text'), '테스트 컨텐츠입니다.')
		self.assertEqual(resp.data.get('school'), self.school.id)


	def test_contents_detail(self):
		
		resp = self.client.get('/api/contents/'+str(self.contents.id)+'/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content)
		self.assertTrue('id' in parseResponse)
		self.assertTrue('creator' in parseResponse)
		self.assertTrue('main_image' in parseResponse)
		self.assertTrue('text' in parseResponse)
		self.assertTrue('school' in parseResponse)
		self.assertTrue('natural_time' in parseResponse)
		self.assertTrue('is_mine' in parseResponse)
		self.assertEqual(parseResponse.get('text'), '초기 컨텐츠입니다.')

	def test_put_contetns(self):

		resp = self.client.get('/api/contents/'+str(self.contents.id)+'/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(resp.content)
		self.assertEqual(parseResponse.get('text'), '초기 컨텐츠입니다.')

		response = self.client.put(
			reverse('contents:detail', kwargs={'contents_id': self.contents.id}), 
			data={'text':'수정된 컨텐츠'}, 
			format='multipart'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		parseResponse = json.loads(response.content)
		self.assertTrue('id' in parseResponse)
		self.assertTrue('creator' in parseResponse)
		self.assertTrue('main_image' in parseResponse)
		self.assertTrue('text' in parseResponse)
		self.assertTrue('school' in parseResponse)
		self.assertEqual(parseResponse.get('text'), '수정된 컨텐츠')

	def test_delete_contents(self):
		contents = Contents.objects.create(school=self.school, creator=self.user, text='초기 컨텐츠입니다.')

		response = self.client.delete(
			reverse('contents:detail', kwargs={'contents_id': contents.id}))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


		resp = self.client.get('/api/contents/'+str(contents.id)+'/')
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

