# Generated by Django 4.0.5 on 2022-07-02 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_alter_bid_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='membership',
        ),
        migrations.AddField(
            model_name='bidder',
            name='balance',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='balance',
            field=models.IntegerField(default=100),
        ),
        migrations.DeleteModel(
            name='MemberFees',
        ),
    ]