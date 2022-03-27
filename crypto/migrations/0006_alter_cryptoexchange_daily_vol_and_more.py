# Generated by Django 4.0 on 2022-03-27 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0005_remove_cryptoexchange_crypto_only_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptoexchange',
            name='daily_vol',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoexchange',
            name='monthly_vol',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
