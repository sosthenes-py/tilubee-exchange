# Generated by Django 4.2.18 on 2025-02-25 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_remove_wallet_algo_remove_wallet_atom_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='uni',
        ),
    ]
