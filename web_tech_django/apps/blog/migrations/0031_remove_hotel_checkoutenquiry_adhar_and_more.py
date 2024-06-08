# Generated by Django 4.1.3 on 2024-06-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_hotel_checkoutenquiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel_checkoutenquiry',
            name='adhar',
        ),
        migrations.AddField(
            model_name='hotel_checkoutenquiry',
            name='aadhar',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='hotel_checkoutenquiry',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='hotel_checkoutenquiry',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
