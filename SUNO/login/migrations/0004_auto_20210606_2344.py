# Generated by Django 2.2.24 on 2021-06-06 18:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210605_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
