# Generated by Django 3.2.24 on 2024-03-09 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_rename_cat_image_category_cat_image1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_image1',
            field=models.ImageField(blank=True, upload_to='photos/categories', verbose_name='Category image'),
        ),
    ]