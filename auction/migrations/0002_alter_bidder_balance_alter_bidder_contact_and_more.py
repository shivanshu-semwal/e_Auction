# Generated by Django 4.0.5 on 2022-07-03 02:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='balance',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='contact',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='seller',
            name='balance',
            field=models.IntegerField(default=1000),
        ),
    ]
