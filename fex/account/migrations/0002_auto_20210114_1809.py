# Generated by Django 3.0 on 2021-01-14 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='freeze_balanca',
            new_name='freeze_balance',
        ),
    ]