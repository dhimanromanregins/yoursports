# Generated by Django 5.0.4 on 2024-04-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='header',
            field=models.TextField(blank=True, null=True),
        ),
    ]
