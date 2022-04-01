# Generated by Django 4.0 on 2022-04-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=128)),
                ('selector', models.CharField(max_length=128)),
            ],
        ),
    ]
