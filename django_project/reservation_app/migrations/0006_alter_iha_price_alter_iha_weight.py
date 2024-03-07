# Generated by Django 5.0.3 on 2024-03-07 05:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0005_iha_image_alter_iha_price_alter_iha_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iha',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='iha',
            name='weight',
            field=models.IntegerField(),
        ),
    ]
