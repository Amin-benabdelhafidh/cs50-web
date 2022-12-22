# Generated by Django 4.1.3 on 2022-12-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_watchlist_items_watchlist_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='catg',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
