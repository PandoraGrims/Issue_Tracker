from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Project(models.Model):
    start_date = models.DateField(verbose_name='Дата начала', default=timezone.now)
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=300, null=True, blank=True, verbose_name='Описание')
    users = models.ManyToManyField(get_user_model(), related_name="projects", blank=True)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        db_table = 'projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        permissions = [
            ('add_users_in_project', 'Добавить юзеров в проект')
        ]


class Status(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Статус")

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        db_table = "statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Тип")

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Task(models.Model):
    summary = models.CharField(max_length=300, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Полное_описание')
    status = models.ForeignKey('webapp.Status', on_delete=models.CASCADE)
    types = models.ManyToManyField('webapp.Type', related_name='tasks', verbose_name='Типы')
    created_at = models.DateField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Время изменения', auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект', related_name='tasks',
                                default=1)

    def __str__(self):
        return f'{self.id}. {self.summary}'

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
