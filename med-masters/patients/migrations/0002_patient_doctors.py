# Generated by Django 5.1.3 on 2024-11-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_alter_doctor_patients'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='doctors',
            field=models.ManyToManyField(related_name='assigned_patients', to='doctors.doctor'),
        ),
    ]