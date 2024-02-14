# Generated by Django 5.0.2 on 2024-02-13 14:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('short_name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'College',
                'verbose_name_plural': 'Colleges',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.college')),
            ],
            options={
                'verbose_name': 'School/Unit',
                'verbose_name_plural': 'Schools/Units',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('MALE', 'male'), ('FEMALE', 'female')], max_length=10)),
                ('type', models.CharField(choices=[('ACADEMIC', 'academic'), ('NON_ACADEMIC', 'non-academic')], default='ACADEMIC', max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.campus')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.unit')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
