# Generated by Django 4.1.3 on 2022-12-01 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_bids_listin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
