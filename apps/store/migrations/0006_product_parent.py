# Generated by Django 4.0.6 on 2022-09-22 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.product'),
        ),
    ]
