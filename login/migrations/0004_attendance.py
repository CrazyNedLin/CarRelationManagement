# Generated by Django 4.2 on 2024-08-27 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=255)),
                ('check_in_time', models.DateTimeField(blank=True, null=True)),
                ('check_out_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
