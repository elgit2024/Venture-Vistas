# Generated by Django 4.0 on 2024-05-29 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_customer_phone_alter_customer_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkoutenquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('second_name', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('district', models.CharField(max_length=50, null=True)),
                ('pin', models.IntegerField(null=True)),
                ('phone', models.IntegerField(null=True)),
            ],
        ),
    ]
