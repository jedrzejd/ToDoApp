from django.test import TestCase
from django.urls import reverse

from mainapp.models import TaskList, Task


class Model_Tests(TestCase):
    def create_TaskList(self, title='only a test'):
        return TaskList.objects.create(title=title)

    def create_Task(self, list, title='only a test', description='opis'):
        return Task.objects.create(title=title, description=description, todo_list=list)

    def update_Task(self, task, title='Dubi dubi du be', description='Hewalump'):
        return self.client.post(
            reverse('task-update', kwargs={
                'list_id': task.todo_list.id,
                'pk': task.id,
            }),
            {
                'todo_list': task.todo_list.id,
                'title': title,
                'description': description,
                'end_date': task.end_date,
             }
        )

    def test_TaskList(self):
        list = self.create_TaskList()
        self.assertTrue(isinstance(list, TaskList))
        self.assertEqual("only a test", list.title)

    def test_create_Task(self):
        list = self.create_TaskList()
        task = self.create_Task(list)
        self.assertTrue(isinstance(task, Task))
        self.assertEqual("only a test", task.title)
        self.assertEqual("opis", task.description)

    def test_update_Task(self):
        list = self.create_TaskList()

        self.assertTrue(isinstance(list, TaskList))
        self.assertEqual("only a test", list.title)

        task = self.create_Task(list)
        response = self.update_Task(task)

        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()

        self.assertEqual(task.title, 'Dubi dubi du be')
        self.assertEqual(task.description, 'Hewalump')
        self.assertTrue(isinstance(task, Task))


class View_Tests(TestCase):
    def test_login(self):
        url = reverse("login")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)