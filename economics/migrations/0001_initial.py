# Generated by Django 4.0 on 2022-04-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('alpha_2', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('currencies', models.ManyToManyField(related_name='currency_country', to='markets.Currency')),
            ],
        ),
    ]
