# Generated by Django 4.2.18 on 2025-03-10 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_userbankaccount_bank_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="userwallet",
            name="key",
            field=models.CharField(default="", max_length=100),
        ),
    ]
