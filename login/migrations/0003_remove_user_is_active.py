# Generated by Django 4.1 on 2024-01-17 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]
