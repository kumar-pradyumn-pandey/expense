# Generated by Django 3.2.4 on 2024-04-27 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_category_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.TextField(null=True),
        ),
    ]
