# Generated by Django 4.1.2 on 2022-11-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_component_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component',
            old_name='location',
            new_name='url_path',
        ),
        migrations.AddField(
            model_name='component',
            name='url_query_string',
            field=models.CharField(default='', max_length=255),
        ),
    ]
