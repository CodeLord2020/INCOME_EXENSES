# Generated by Django 4.1.7 on 2023-06-21 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ap1', '0002_rename_owner_income_owner_in'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='owner_in',
            new_name='owner',
        ),
    ]
