from django.test import TestCase
from tasks.models import Task
from datetime import date, timedelta


class ActorModelTestCase(TestCase):


    def test_create_task(self):
        actor = Task.objects.create(
            title = 'Test task',
            description = 'Description test task',
            due_date = date.today() + timedelta(days=5) 
        )
        actor.save()
        self.assertEqual(actor.title, 'Test task')
