# Generated by Django 5.1.2 on 2024-11-18 02:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0001_initial"),
        ("doctors", "0002_alter_doctor_dob"),
        ("patients", "0003_recordeddata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="appointments",
                to="patients.patient",
            ),
        ),
        migrations.RemoveField(
            model_name="appointment",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="appointment",
            name="doctor_username",
        ),
        migrations.AddField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="appointments",
                to="doctors.doctor",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="room_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="day",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Patient",
        ),
    ]
