# Generated by Django 4.1.2 on 2022-11-07 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_delete_conversionurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='conversion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.componentconversionevent'),
        ),
    ]