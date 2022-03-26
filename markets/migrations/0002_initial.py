# Generated by Django 4.0 on 2022-03-26 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
        ('economics', '0002_initial'),
        ('crypto', '0001_initial'),
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_creator', to='website.account'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='followers',
            field=models.ManyToManyField(related_name='watchlist_followers', to='website.Account'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto.cryptoexchange'),
        ),
        migrations.AddField(
            model_name='ticker',
            name='base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_base', to='markets.asset'),
        ),
        migrations.AddField(
            model_name='ticker',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markets.market'),
        ),
        migrations.AddField(
            model_name='ticker',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_quote', to='markets.asset'),
        ),
        migrations.AddField(
            model_name='portfolioamounts',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolioamounts_asset', to='markets.asset'),
        ),
        migrations.AddField(
            model_name='market',
            name='countries',
            field=models.ManyToManyField(to='economics.Country'),
        ),
        migrations.AddField(
            model_name='market',
            name='tickers',
            field=models.ManyToManyField(related_name='market_tickers', to='markets.Ticker'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(to='website.Tag'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_currency', to='markets.currency'),
        ),
        migrations.AddField(
            model_name='portfolioamounts',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolioamounts_portfolio', to='markets.portfolio'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='amounts',
            field=models.ManyToManyField(through='markets.PortfolioAmounts', to='markets.Asset'),
        ),
        migrations.AddField(
            model_name='market',
            name='currencies',
            field=models.ManyToManyField(to='markets.Currency'),
        ),
        migrations.AddField(
            model_name='currency',
            name='issuer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='currency_issuer', to='economics.country'),
        ),
    ]
