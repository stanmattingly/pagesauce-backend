# Generated by Django 4.1.2 on 2022-11-01 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_component_universal_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='stripe_account_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
