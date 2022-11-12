# Generated by Django 4.1.2 on 2022-10-25 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_groupfeature_users_price_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('-', '-'), ('view', 'View'), ('hover', 'Hover'), ('select', 'Select'), ('unselect', 'Un-select'), ('signup_hover', 'Sing Up Hover'), ('signup_click', 'Sign Up Click'), ('purchase', 'Purchase')], default='-', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('features', models.ManyToManyField(related_name='feature_analytics', to='core.groupfeature')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_analytics', to='core.price')),
                ('group_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='description_analytics', to='core.pricegroupdescription')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_analytics', to='core.price')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_analytics', to='core.analyticsuser')),
            ],
        ),
        migrations.AddField(
            model_name='pricegroup',
            name='downs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pricegroup',
            name='hotness',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pricegroup',
            name='ups',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='PriceAction',
        ),
    ]
