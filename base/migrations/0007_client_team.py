# Generated by Django 5.0.3 on 2024-05-16 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_client_project_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.team'),
        ),
    ]
