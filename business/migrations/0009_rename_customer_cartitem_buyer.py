# Generated by Django 3.2.3 on 2022-03-05 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_cartitem_order_shippingaddress_stripepayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='customer',
            new_name='buyer',
        ),
    ]
