# Generated by Django 4.2.18 on 2025-01-30 00:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_alter_conversion_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversion',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
