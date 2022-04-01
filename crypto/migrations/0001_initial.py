# Generated by Django 4.0 on 2022-03-27 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('symbol', models.CharField(max_length=32)),
                ('url', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('hash_algorithm', models.CharField(blank=True, max_length=64, null=True)),
                ('proof_type', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('crypto_only', models.BooleanField()),
                ('grade', models.CharField(choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'NA')], max_length=3)),
                ('url', models.CharField(max_length=128)),
                ('daily_vol', models.FloatField()),
                ('monthly_vol', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Portfolio', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioAmounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=32)),
                ('quote', models.CharField(max_length=32)),
                ('bid', models.FloatField()),
                ('ask', models.FloatField()),
                ('daily_low', models.FloatField()),
                ('daily_high', models.FloatField()),
                ('hourly_delta', models.FloatField()),
                ('daily_delta', models.FloatField()),
                ('weekly_delta', models.FloatField()),
                ('daily_vol', models.FloatField()),
                ('monthly_vol', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Watchlist', max_length=32)),
            ],
        ),
    ]