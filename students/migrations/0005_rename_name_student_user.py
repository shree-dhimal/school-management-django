# Generated by Django 5.0.3 on 2024-04-03 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_remove_subjects_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='name',
            new_name='user',
        ),
    ]