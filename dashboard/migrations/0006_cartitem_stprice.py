# Generated by Django 4.2.8 on 2023-12-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_item_retired"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="stprice",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]