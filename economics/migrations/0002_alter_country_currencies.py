# Generated by Django 4.0 on 2022-03-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='currencies',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
