# Generated by Django 4.1.1 on 2022-09-17 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_bider_bid_bidder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.bid'),
        ),
    ]
