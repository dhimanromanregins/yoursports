# Generated by Django 5.0.4 on 2024-04-14 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0002_pricing_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing',
            name='amount',
            field=models.CharField(max_length=2000),
        ),
    ]