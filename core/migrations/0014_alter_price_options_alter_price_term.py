# Generated by Django 4.1.2 on 2022-10-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_pricegroup_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['group__name', 'price', 'term']},
        ),
        migrations.AlterField(
            model_name='price',
            name='term',
            field=models.CharField(choices=[('mo', 'Monthly'), ('yr', 'Yearly')], default='mo', max_length=25),
        ),
    ]