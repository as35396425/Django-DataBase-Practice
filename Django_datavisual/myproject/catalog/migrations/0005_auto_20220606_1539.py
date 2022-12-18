# Generated by Django 2.2.6 on 2022-06-06 07:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20220605_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]