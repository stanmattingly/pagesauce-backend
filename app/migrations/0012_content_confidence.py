# Generated by Django 4.1.2 on 2022-11-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_contentcluster_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='confidence',
            field=models.FloatField(default=0),
        ),
    ]