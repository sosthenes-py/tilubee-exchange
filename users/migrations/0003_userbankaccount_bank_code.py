# Generated by Django 4.2.18 on 2025-02-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_appuser_last_access"),
    ]

    operations = [
        migrations.AddField(
            model_name="userbankaccount",
            name="bank_code",
            field=models.CharField(default="", max_length=10),
        ),
    ]
