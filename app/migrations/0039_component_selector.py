# Generated by Django 4.1.2 on 2022-11-12 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_remove_component_current_campaign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='selector',
            field=models.TextField(blank=True, default=''),
        ),
    ]
