# Generated by Django 3.2.5 on 2021-07-18 19:09

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('award', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('landingpage', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('description', models.CharField(max_length=300)),
                ('link', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='award.profile')),
            ],
        ),
    ]
