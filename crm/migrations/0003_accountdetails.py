# Generated by Django 4.2.18 on 2025-03-01 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0002_alter_adminuser_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(default="", max_length=20, null=True)),
                ("bank", models.CharField(default="", max_length=20, null=True)),
                ("name", models.CharField(default="", max_length=20, null=True)),
                ("uid", models.CharField(default="", max_length=20, null=True)),
                ("account_type", models.CharField(default="bank", max_length=10)),
                ("platform", models.CharField(default="", max_length=10)),
            ],
        ),
    ]
