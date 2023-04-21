# Generated by Django 4.1.7 on 2023-04-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_portfoliovalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='value',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='portfolioasset',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='portfolioasset',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='portfoliovalue',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]