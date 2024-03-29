# Generated by Django 4.1.2 on 2022-11-09 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_remove_conversion_components'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='go_live_date',
        ),
        migrations.CreateModel(
            name='ComponentCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='app.component')),
            ],
        ),
    ]
