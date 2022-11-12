# Generated by Django 4.1.2 on 2022-11-01 08:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_analytic_created_at_contentcluster'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='content_cluster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='app.contentcluster'),
        ),
        migrations.AddField(
            model_name='contentcluster',
            name='universal_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
