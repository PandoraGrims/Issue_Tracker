from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Статус")

    def __str__(self):
        return f'{self.id}. {self.name}'


class Type(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Тип")

    def __str__(self):
        return f'{self.id}. {self.name}'


class Task(models.Model):
    summary = models.CharField(max_length=300, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Полное_описание')
    status = models.ForeignKey('webapp.Status', on_delete=models.CASCADE)
    task_types = models.ManyToManyField('webapp.Type')
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время изменения', auto_now=True)

    def __str__(self):
        return f'{self.id}. {self.summary}'
