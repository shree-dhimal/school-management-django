# Generated by Django 5.0.3 on 2024-04-03 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_subjects_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='date_of_birth',
        ),
    ]
