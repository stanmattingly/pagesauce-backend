# Generated by Django 4.1.2 on 2022-11-05 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_analytic_is_conversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='element_class',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='component',
            name='element_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
