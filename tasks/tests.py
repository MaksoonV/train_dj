from django.test import Client, TestCase
from django.urls import reverse
from .models import Task


class TaskFlowTests(TestCase):
    def test_create_toggle_delete(self):
        home = reverse("tasks:index")
        self.assertContains(self.client.get(home), "Пока пусто")
        self.assertRedirects(self.client.post(home, {"title": "Изучить Django"}), home)
        task = Task.objects.get()
        self.assertContains(self.client.get(home), task.title)
        toggle = reverse("tasks:toggle", args=[task.pk])
        delete = reverse("tasks:delete", args=[task.pk])
        self.assertEqual(self.client.get(toggle).status_code, 405)
        self.assertEqual(self.client.get(delete).status_code, 405)
        self.client.post(toggle)
        task.refresh_from_db()
        self.assertTrue(task.done)
        self.client.post(toggle)
        task.refresh_from_db()
        self.assertFalse(task.done)
        self.client.post(delete)
        self.assertFalse(Task.objects.exists())

    def test_invalid_input(self):
        for title in ["", "   ", "a" * 201]:
            response = self.client.post(reverse("tasks:index"), {"title": title})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertFalse(Task.objects.exists())

    def test_missing_task(self):
        self.assertEqual(self.client.post(reverse("tasks:toggle", args=[999])).status_code, 404)
        self.assertEqual(self.client.post(reverse("tasks:delete", args=[999])).status_code, 404)

    def test_csrf_required_and_valid_submission(self):
        client = Client(enforce_csrf_checks=True)
        home = reverse("tasks:index")
        self.assertEqual(client.post(home, {"title": "Без токена"}).status_code, 403)
        client.get(home)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(home, {"title": "С токеном", "csrfmiddlewaretoken": token}).status_code, 302)

    def test_html_is_escaped(self):
        Task.objects.create(title="<script>alert(1)</script>")
        response = self.client.get(reverse("tasks:index"))
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")
