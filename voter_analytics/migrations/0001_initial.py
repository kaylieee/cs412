# Generated by Django 5.1.6 on 2025-04-06 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.TextField()),
                ('first_name', models.TextField()),
                ('street_number', models.IntegerField()),
                ('street_name', models.TextField()),
                ('zip_code', models.IntegerField()),
                ('apartment_number', models.TextField()),
                ('dob', models.DateField()),
                ('registration_date', models.DateField()),
                ('party', models.CharField(max_length=2)),
                ('precinct', models.CharField(max_length=2)),
                ('v20state', models.BooleanField()),
                ('v21town', models.BooleanField()),
                ('v21primary', models.BooleanField()),
                ('v22general', models.BooleanField()),
                ('v23town', models.BooleanField()),
            ],
        ),
    ]
