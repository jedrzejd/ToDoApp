from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class TaskList(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Nazwa Listy')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              null=True
                              )

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tytuł zadania')
    description = models.TextField(null=True, blank=True, verbose_name='Opis zadania')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data stworzenia')
    end_date = models.DateTimeField(default=one_week_hence, verbose_name='Data zakończenia zadania')
    todo_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, verbose_name='Nazwa listy')

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return f"{self.title}:  {self.end_date.date()}"
