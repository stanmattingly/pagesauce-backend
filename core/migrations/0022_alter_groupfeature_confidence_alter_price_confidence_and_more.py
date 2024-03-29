# Generated by Django 4.1.2 on 2022-11-05 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_groupfeature_confidence_price_confidence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupfeature',
            name='confidence',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='price',
            name='confidence',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='pricegroup',
            name='confidence',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='pricegroupdescription',
            name='confidence',
            field=models.FloatField(default=1),
        ),
    ]
