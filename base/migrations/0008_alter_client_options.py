# Generated by Django 5.0.3 on 2024-05-16 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_client_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['active', 'name']},
        ),
    ]
