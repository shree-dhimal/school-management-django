# Generated by Django 5.0.3 on 2024-04-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
