# Generated by Django 4.0.6 on 2022-09-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_status_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_date_changed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
