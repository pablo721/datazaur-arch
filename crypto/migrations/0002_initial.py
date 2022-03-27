# Generated by Django 4.0 on 2022-03-27 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crypto', '0001_initial'),
        ('economics', '0001_initial'),
        ('markets', '0001_initial'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_creator', to='website.account'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_currency', to='markets.currency'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='followers',
            field=models.ManyToManyField(related_name='watchlist_followers', to='website.Account'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_source', to='crypto.cryptoexchange'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='watched_coins',
            field=models.ManyToManyField(related_name='watchlist_coins', to='crypto.Cryptocurrency'),
        ),
        migrations.AddField(
            model_name='portfolioamounts',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolioamounts_coin', to='crypto.cryptocurrency'),
        ),
        migrations.AddField(
            model_name='portfolioamounts',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolioamounts_portfolio', to='crypto.portfolio'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='amounts',
            field=models.ManyToManyField(related_name='portfolio_amounts', through='crypto.PortfolioAmounts', to='crypto.Cryptocurrency'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_currency', to='markets.currency'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_owner', to='website.account'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portf_coins',
            field=models.ManyToManyField(related_name='portfolio_coins', to='crypto.Cryptocurrency'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_source', to='crypto.cryptoexchange'),
        ),
        migrations.AddField(
            model_name='cryptoexchange',
            name='countries',
            field=models.ManyToManyField(to='economics.Country'),
        ),
        migrations.AddField(
            model_name='cryptoexchange',
            name='currencies',
            field=models.ManyToManyField(to='markets.Currency'),
        ),
        migrations.AddField(
            model_name='cryptoexchange',
            name='tickers',
            field=models.ManyToManyField(related_name='market_tickers', to='crypto.Cryptocurrency'),
        ),
    ]
