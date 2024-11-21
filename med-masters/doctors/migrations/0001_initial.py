# Generated by Django 5.1.3 on 2024-11-21 08:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_username', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('day', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(max_length=50)),
                ('DOB', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('start_year_of_practice', models.IntegerField()),
                ('availability_hours', models.JSONField(blank=True, default=list)),
                ('specialization', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('hospital', models.CharField(max_length=255)),
                ('patients', models.ManyToManyField(related_name='doctors', to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_booked', models.BooleanField(default=False)),
                ('day_name', models.CharField(blank=True, max_length=50, null=True)),
                ('parent_start_time', models.TimeField(blank=True, null=True)),
                ('parent_end_time', models.TimeField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to='doctors.doctor')),
            ],
        ),
    ]
