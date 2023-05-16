from django.contrib import admin
from django.db.models.functions import datetime
from django.utils import timezone

from mainapp.models import Task, TaskList


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'end_date')
    search_fields = ('title',)
    list_filter = ['created_date']

    @admin.display(
        boolean=True,
        ordering='created_date',
        description='Created recently',
    )
    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_date <= now


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'countTask'
    )
    list_filter = ('owner',)
    search_fields = ('title',)

    def countTask(self, obj):
        return obj.task_set.count()

    countTask.short_description = 'Liczba zadań na liście'