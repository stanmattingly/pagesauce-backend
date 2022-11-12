# Generated by Django 4.1.2 on 2022-11-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupfeature',
            name='confidence',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='price',
            name='confidence',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pricegroup',
            name='confidence',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pricegroupdescription',
            name='confidence',
            field=models.FloatField(default=0),
        ),
    ]
