# Generated by Django 4.0.5 on 2022-06-30 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_rename_images_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='items_pics/'),
        ),
    ]