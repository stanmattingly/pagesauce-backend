# Generated by Django 4.1.2 on 2022-11-07 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_alter_analytic_conversion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analytic',
            name='conversion',
        ),
        migrations.AlterField(
            model_name='contentcluster',
            name='contents',
            field=models.ManyToManyField(blank=True, related_name='clusters', to='app.content'),
        ),
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('components', models.ManyToManyField(related_name='conversions', to='app.component')),
                ('content_cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversions', to='app.contentcluster')),
                ('contents', models.ManyToManyField(related_name='conversions', to='app.content')),
                ('conversion_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversions', to='app.componentconversionevent')),
            ],
        ),
    ]
