# Generated by Django 4.0.2 on 2022-02-27 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlistings'),
        ),
    ]
