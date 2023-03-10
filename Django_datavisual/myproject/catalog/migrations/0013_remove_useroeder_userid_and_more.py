# Generated by Django 4.1.3 on 2022-12-05 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0012_orderproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useroeder',
            name='userID',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='productUserOrder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_userBuy', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
