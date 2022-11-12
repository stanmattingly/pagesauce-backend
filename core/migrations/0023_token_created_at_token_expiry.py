# Generated by Django 4.1.2 on 2022-11-05 07:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_groupfeature_confidence_alter_price_confidence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]