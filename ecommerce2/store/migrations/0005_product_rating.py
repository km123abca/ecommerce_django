# Generated by Django 3.0.8 on 2020-07-28 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2),
        ),
    ]
