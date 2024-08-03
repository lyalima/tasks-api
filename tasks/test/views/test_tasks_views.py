from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import date, timedelta
from rest_framework_simplejwt.tokens import RefreshToken


class TaskAPITestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url_list_create = reverse('task-create-list-view')
        self.token = self.get_token_for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task.',
            due_date=date.today() + timedelta(days=5),
            created_at=date.today(),
            updated_at=date.today()
        )


    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


    def test_create_task(self):
        payload = {
            'title': 'New Task',
            'description': 'Task description',
            'due_date': (date.today() + timedelta(days=10)).isoformat()
        }

        response = self.client.post(self.url_list_create, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title=payload.get('title')).exists())


    def test_create_task_invalid_due_date(self):
        payload = {
            'title': 'Invalid Task',
            'description': 'Task description',
            'due_date': (date.today() - timedelta(days=1)).isoformat()
        }

        response = self.client.post(self.url_list_create, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)
        self.assertFalse(Task.objects.filter(title=payload.get('title')).exists())


    def test_list_tasks(self):
        response = self.client.get(self.url_list_create, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_filter_tasks_by_title(self):
        response = self.client.get(self.url_list_create, {'title': 'Test Task'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')


    def test_filter_tasks_by_due_date(self):
        response = self.client.get(self.url_list_create, {'due_date': self.task.due_date.isoformat()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['due_date'], self.task.due_date.isoformat())


    def test_update_task(self):
        url_detail = reverse('task-detail-view', args=[self.task.id])
        payload = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'due_date': (date.today() + timedelta(days=15)).isoformat()
        }

        response = self.client.put(url_detail, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, payload['title'])
        self.assertEqual(self.task.description, payload['description'])
        self.assertEqual(self.task.due_date.isoformat(), payload['due_date'])


    def test_delete_task(self):
        url_detail = reverse('task-detail-view', args=[self.task.id])

        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.task.refresh_from_db()
        self.assertTrue(self.task.deleted)
