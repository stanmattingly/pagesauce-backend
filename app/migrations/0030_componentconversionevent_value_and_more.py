# Generated by Django 4.1.2 on 2022-11-07 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_component_go_live_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentconversionevent',
            name='value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='component',
            name='element_type',
            field=models.CharField(choices=[('-', '-'), ('BUTTON', 'Button'), ('A', 'Button'), ('P', 'Paragraph'), ('H1', 'Heading'), ('H2', 'Heading'), ('H3', 'Heading'), ('H4', 'Heading'), ('H5', 'Heading'), ('H6', 'Heading'), ('DIV', 'Text'), ('SPAN', 'Text'), ('submit', 'Button')], default='-', max_length=50),
        ),
        migrations.DeleteModel(
            name='Conversion',
        ),
    ]