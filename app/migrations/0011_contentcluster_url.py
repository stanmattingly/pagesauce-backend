# Generated by Django 4.1.2 on 2022-11-01 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_analytic_content_cluster_contentcluster_universal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentcluster',
            name='url',
            field=models.URLField(null=True),
        ),
    ]