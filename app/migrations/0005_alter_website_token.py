# Generated by Django 4.1.2 on 2022-11-01 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_token'),
        ('app', '0004_alter_website_stripe_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='token',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='website_object', to='core.token'),
        ),
    ]
