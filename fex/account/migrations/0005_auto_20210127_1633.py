# Generated by Django 3.0 on 2021-01-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210123_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitlyassigning them.', verbose_name='superuser status'),
        ),
    ]