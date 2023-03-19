# Generated by Django 4.0.6 on 2023-03-16 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('order_id', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]