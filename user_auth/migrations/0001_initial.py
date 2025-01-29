# Generated by Django 4.2.18 on 2025-01-26 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=10)),
                ('verified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
