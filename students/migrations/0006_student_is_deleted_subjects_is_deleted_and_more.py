# Generated by Django 5.0.3 on 2024-04-03 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_rename_name_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subjects',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Management', 'Management')], default='Teacher', max_length=50),
        ),
    ]
