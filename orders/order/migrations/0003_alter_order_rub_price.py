# Generated by Django 4.0.6 on 2023-03-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_rub_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='rub_price',
            field=models.FloatField(),
        ),
    ]
