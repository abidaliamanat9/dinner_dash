# Generated by Django 4.2.8 on 2024-01-03 12:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_alter_cartitem_stprice_alter_item_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="stprice",
        ),
    ]
