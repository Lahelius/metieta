# Generated by Django 5.0.3 on 2024-05-16 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_client_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['-active', 'name']},
        ),
    ]
