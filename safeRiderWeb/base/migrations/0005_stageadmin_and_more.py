# Generated by Django 5.0.3 on 2024-04-04 22:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_national_id_number_customer_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StageAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='phone_number',
            new_name='customer_name',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='transaction_id',
            new_name='fare_transaction_id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='boda_username',
        ),
        migrations.RemoveField(
            model_name='emergencycontact',
            name='emergency_name',
        ),
        migrations.AddField(
            model_name='customer',
            name='boda_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_phone_number',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.location'),
        ),
        migrations.AddField(
            model_name='emergencycontact',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
