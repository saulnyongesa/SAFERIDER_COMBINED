# Generated by Django 5.0.3 on 2024-04-06 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base2', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminUser',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
    ]
