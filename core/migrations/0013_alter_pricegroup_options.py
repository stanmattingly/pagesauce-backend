# Generated by Django 4.1.2 on 2022-10-30 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_pricegroup_term_price_term'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricegroup',
            options={'ordering': ['name']},
        ),
    ]
