# Generated by Django 4.2.3 on 2023-11-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_user_earnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='Apex Engine User'),
        ),
    ]
