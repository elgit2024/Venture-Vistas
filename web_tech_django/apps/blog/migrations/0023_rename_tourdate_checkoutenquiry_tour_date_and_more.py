# Generated by Django 4.0 on 2024-06-02 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_checkoutenquiry_tourdate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutenquiry',
            old_name='tourdate',
            new_name='tour_date',
        ),
        migrations.RenameField(
            model_name='checkoutenquiry',
            old_name='tourtravellers',
            new_name='tour_travellers',
        ),
    ]
