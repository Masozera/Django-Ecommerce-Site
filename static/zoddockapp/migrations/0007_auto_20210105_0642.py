# Generated by Django 3.1.3 on 2021-01-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoddockapp', '0006_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
