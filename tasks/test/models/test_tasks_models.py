from django.test import TestCase
from tasks.models import Task
from datetime import date, timedelta


class ActorModelTestCase(TestCase):

    def test_create_task(self):
        task = Task.objects.create(
            title = 'Test task',
            description = 'Description test task',
            due_date = date.today() + timedelta(days=5) 
        )        
        task.save()
        self.assertEqual(task.title, 'Test task')
