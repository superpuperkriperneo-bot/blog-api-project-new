from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from . models import Post

class PostApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password'
        )
        self.post = Post.objects.create(
            author = self.user,
            title = 'test_title',
            content = 'test_content'
        )

    def test_model_str_resresentation(self):
        self.assertEqual(str(self.post), 'test_title')

    def test_list_post_unauthentificated(self):
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'test_title')

    def test_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data={'title':'new_post', 'content':'new_content'}
        response=self.client.post('/api/v1/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, 'new_post')

    def test_create_post_unauthenticated(self):
        data={'title':'not_permitted_title', 'content':'not_permitted_content'}
        response=self.client.post('/api/v1/posts/', data)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_update_post_by_author(self):
        self.client.force_authenticate(user=self.user)
        updated_data={'title':'updated_title', 'content':'updated_content'}
        response = self.client.put(f'/api/v1/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'updated_title')

    def test_update_post_by_another_user(self):
        another_user = User.objects.create_user(
            username = 'anotheruser',
            password = 'anotherpassword'
        )

        self.client.force_authenticate(user=another_user)
        updated_data = {'title': 'stop_title'}
        response=self.client.put(f'/api/v1/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)