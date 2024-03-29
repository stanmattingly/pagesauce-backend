# Generated by Django 4.1.2 on 2022-11-01 08:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_action_analytic_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ContentCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('analytic_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.analyticuser')),
                ('contents', models.ManyToManyField(related_name='clusters', to='app.content')),
            ],
        ),
    ]
