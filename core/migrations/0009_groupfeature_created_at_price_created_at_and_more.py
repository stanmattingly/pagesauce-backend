# Generated by Django 4.1.2 on 2022-10-25 08:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_analyticrecord_group_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupfeature',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pricegroup',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pricegroupdescription',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='analyticrecord',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='analyticsuser',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='groupfeature',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='features', to='core.analyticsuser'),
        ),
        migrations.AlterField(
            model_name='price',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='prices', to='core.analyticsuser'),
        ),
        migrations.AlterField(
            model_name='pricegroupdescription',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='descriptions', to='core.analyticsuser'),
        ),
    ]