# Generated by Django 4.0.6 on 2022-08-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('paid_amount', models.FloatField(blank=True, null=True)),
                ('used_coupon', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_intent', models.CharField(max_length=255)),
                ('shipped_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
