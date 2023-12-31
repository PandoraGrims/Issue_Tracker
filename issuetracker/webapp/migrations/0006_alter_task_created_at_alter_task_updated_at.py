# Generated by Django 5.0 on 2023-12-25 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_project_options_alter_status_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Время изменения'),
        ),
    ]
