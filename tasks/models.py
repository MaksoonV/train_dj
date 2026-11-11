from django.db import models


class Task(models.Model):
    """Одна запись в таблице: текст задачи и отметка о выполнении."""
    title = models.CharField("Задача", max_length=200)
    done = models.BooleanField("Выполнена", default=False)

    def __str__(self):
        return self.title
