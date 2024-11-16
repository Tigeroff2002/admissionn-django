# Generated by Django 5.1.3 on 2024-11-16 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='abiturient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('has_diplom_original', models.BooleanField(default=False)),
                ('is_requested', models.BooleanField(default=False)),
                ('is_enrolled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'abiturients',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='direction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('caption', models.CharField(max_length=255)),
                ('budget_places_number', models.IntegerField()),
                ('min_ball', models.IntegerField()),
                ('is_filled', models.BooleanField(default=False)),
                ('is_finalized', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'directions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='abiturient_direction_link',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('place', models.IntegerField(default=0)),
                ('mark', models.IntegerField(default=0)),
                ('admission_status', models.CharField(default='request_in_progress', max_length=255)),
                ('prioritet_number', models.IntegerField(default=1)),
                ('has_diplom_original', models.BooleanField(default=False)),
                ('abiturient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission_django.abiturient')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission_django.direction')),
            ],
            options={
                'db_table': 'abiturient_direction_links',
                'managed': True,
            },
        ),
    ]