# Generated by Django 5.0 on 2023-12-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='type',
        ),
        migrations.AddField(
            model_name='task',
            name='task_types',
            field=models.ManyToManyField(to='webapp.type'),
        ),
    ]
