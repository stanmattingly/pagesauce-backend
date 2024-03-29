# Generated by Django 4.1.2 on 2022-10-30 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_remove_pricegroup_owner_pricegroup_stripe_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripeaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
