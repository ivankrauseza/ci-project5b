# Generated by Django 4.1.13 on 2024-05-24 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_salesorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(choices=[('1', 'Preparing'), ('2', 'Shipped'), ('3', 'Complete')], default='', max_length=1),
        ),
    ]
