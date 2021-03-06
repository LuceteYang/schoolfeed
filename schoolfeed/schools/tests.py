import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from schoolfeed.schools.models import Member, School, Contents
from schoolfeed.users.models import User


class SchoolsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='chevy@chase.com', username='sanghwan', password='chevyspassword', name='박상환')

        url = reverse('rest_framework:rest_login')
        resp = self.client.post(url, {'username': 'sanghwan', 'password': 'chevyspassword'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.school = School.objects.create(name='금호고등학교', location='광주광역시 북구 금호로 100', creator=self.user)
        Member.objects.create(school=self.school, member=self.user, role=1)
        self.contents = Contents.objects.create(school=self.school, creator=self.user, text='초기 컨텐츠입니다.')

    def test_create_school(self):
        resp = self.client.post('/api/schools/', {'name': '태봉초등학교', 'location': '광주광역시 북구 청계로 33'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in resp.data)
        self.assertTrue('image' in resp.data)
        self.assertTrue('is_subscribed' in resp.data)
        self.assertEqual(resp.data.get('name'), '태봉초등학교')
        self.assertEqual(resp.data.get('location'), '광주광역시 북구 청계로 33')

    def test_search_school(self):
        resp = self.client.get('/api/schools/search/?school_name=금호')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(parseResponse), 1)
        self.assertEqual(parseResponse[0].get('name'), '금호고등학교')

    def test_school_detail(self):
        school = School.objects.first()
        resp = self.client.get('/api/schools/' + str(school.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertTrue('id' in parseResponse)
        self.assertTrue('name' in parseResponse)
        self.assertTrue('image' in parseResponse)
        self.assertTrue('location' in parseResponse)
        self.assertTrue('is_subscribed' in parseResponse)
        self.assertTrue('is_manager' in parseResponse)
        self.assertTrue('contents' in parseResponse)

    def test_put_school(self):

        resp = self.client.get('/api/schools/' + str(self.school.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertTrue('id' in parseResponse)
        self.assertTrue('name' in parseResponse)
        self.assertTrue('image' in parseResponse)
        self.assertTrue('location' in parseResponse)
        self.assertTrue('is_subscribed' in parseResponse)
        self.assertTrue('is_manager' in parseResponse)
        self.assertTrue('contents' in parseResponse)
        self.assertEqual(parseResponse.get('name'), '금호고등학교')
        self.assertEqual(parseResponse.get('location'), '광주광역시 북구 금호로 100')

        response = self.client.put(
            reverse('schools:detail', kwargs={'school_id': self.school.id}),
            data={'name': '수정된학교이름', 'location': '새로운 주소'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in parseResponse)
        self.assertTrue('name' in parseResponse)
        self.assertTrue('image' in parseResponse)
        self.assertTrue('location' in parseResponse)
        self.assertTrue('is_subscribed' in parseResponse)
        self.assertEqual(parseResponse.get('name'), '수정된학교이름')
        self.assertEqual(parseResponse.get('location'), '새로운 주소')

    def test_delete_school(self):
        school = School.objects.create(name='새로운 학교', location='새로운 주소', creator=self.user)
        Member.objects.create(school=school, member=self.user, role=1)
        response = self.client.delete(
            reverse('schools:detail', kwargs={'school_id': school.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get('/api/schools/' + str(school.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_school_contents(self):
        resp = self.client.get('/api/schools/' + str(self.school.id) + '/contents/?last_contents_id=0', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(parseResponse), 1)

    def test_school_subscribes(self):
        resp = self.client.post('/api/schools/' + str(self.school.id) + '/subscribes/')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get('/api/schools/' + str(self.school.id) + '/subscribes/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(parseResponse), 1)

        resp = self.client.delete('/api/schools/' + str(self.school.id) + '/unsubscribes/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        resp = self.client.get('/api/schools/' + str(self.school.id) + '/subscribes/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(parseResponse), 0)

    def test_create_contents(self):
        resp = self.client.post('/api/schools/' + str(self.school.id) + '/contents/', {'text': '테스트 컨텐츠입니다.'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in resp.data)
        self.assertTrue('creator' in resp.data)
        self.assertTrue('main_image' in resp.data)
        self.assertTrue('text' in resp.data)
        self.assertTrue('school' in resp.data)
        self.assertEqual(resp.data.get('text'), '테스트 컨텐츠입니다.')
        self.assertEqual(resp.data.get('school'), self.school.id)

    def test_contents_detail(self):
        resp = self.client.get(reverse('schools:contentsDetail', kwargs={'school_id': self.school.id, 'contents_id': self.contents.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertTrue('id' in parseResponse)
        self.assertTrue('creator' in parseResponse)
        self.assertTrue('main_image' in parseResponse)
        self.assertTrue('text' in parseResponse)
        self.assertTrue('school' in parseResponse)
        self.assertTrue('natural_time' in parseResponse)
        self.assertTrue('is_mine' in parseResponse)
        self.assertEqual(parseResponse.get('text'), '초기 컨텐츠입니다.')

    def test_put_contetns(self):
        resp = self.client.get(reverse('schools:contentsDetail', kwargs={'school_id': self.school.id, 'contents_id': self.contents.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(parseResponse.get('text'), '초기 컨텐츠입니다.')

        response = self.client.put(
            reverse('schools:contentsDetail', kwargs={'school_id': self.school.id, 'contents_id': self.contents.id}),
            data={'text': '수정된 컨텐츠'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parseResponse = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in parseResponse)
        self.assertTrue('creator' in parseResponse)
        self.assertTrue('main_image' in parseResponse)
        self.assertTrue('text' in parseResponse)
        self.assertTrue('school' in parseResponse)
        self.assertEqual(parseResponse.get('text'), '수정된 컨텐츠')

    def test_delete_contents(self):
        contents = Contents.objects.create(school=self.school, creator=self.user, text='초기 컨텐츠입니다.')
        response = self.client.delete(
            reverse('schools:contentsDetail', kwargs={'school_id': self.school.id, 'contents_id': contents.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(reverse('schools:contentsDetail', kwargs={'school_id': self.school.id, 'contents_id': contents.id}))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
