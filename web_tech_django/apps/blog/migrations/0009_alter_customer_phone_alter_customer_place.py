# Generated by Django 4.0 on 2024-05-29 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_customer_phone_alter_customer_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='place',
            field=models.CharField(max_length=50),
        ),
    ]
