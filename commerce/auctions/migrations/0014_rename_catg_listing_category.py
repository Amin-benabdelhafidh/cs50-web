# Generated by Django 4.1.3 on 2022-12-14 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_category_listing_catg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='catg',
            new_name='category',
        ),
    ]
