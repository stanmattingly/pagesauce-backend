# Generated by Django 4.1.2 on 2022-11-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_analytic_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='css_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
