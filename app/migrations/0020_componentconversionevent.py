# Generated by Django 4.1.2 on 2022-11-05 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_rename_location_component_url_path_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentConversionEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('-', '-'), ('click', 'Click'), ('focus', 'Select'), ('blur', 'Blur'), ('mouseover', 'Hover'), ('mouseleave', 'Leave'), ('select', 'Select'), ('submit', 'Submit'), ('copy', 'Copy'), ('view', 'View'), ('conversion', 'Conversion')], default='click', max_length=50)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.component')),
            ],
        ),
    ]
