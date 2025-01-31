# Generated by Django 4.2.18 on 2025-01-29 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_conversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversion',
            name='status',
            field=models.CharField(default='pending', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(default='completed', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(default='deposit', max_length=10),
            preserve_default=False,
        ),
    ]
