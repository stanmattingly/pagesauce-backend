# Generated by Django 4.1.2 on 2022-11-01 06:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_token'),
        ('app', '0005_alter_website_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticuser',
            name='website',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.website'),
        ),
        migrations.AlterField(
            model_name='analytic',
            name='action',
            field=models.CharField(choices=[('-', '-'), ('click', 'Click'), ('focus', 'Focus'), ('blur', 'Blur'), ('mouseover', 'Hover'), ('mouseleave', 'Leave'), ('select', 'Select'), ('submit', 'Submit'), ('copy', 'Copy')], default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='component',
            name='universal_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='website',
            name='token',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='website', to='core.token'),
        ),
    ]
