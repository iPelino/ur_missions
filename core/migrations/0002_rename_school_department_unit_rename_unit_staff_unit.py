# Generated by Django 5.0.2 on 2024-02-14 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='school',
            new_name='unit',
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='Unit',
            new_name='unit',
        ),
    ]