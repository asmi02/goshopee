# Generated by Django 4.1 on 2022-10-15 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productshopping', '0003_remove_product_size_sizes_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='qty',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1000, null=True),
        ),
    ]
