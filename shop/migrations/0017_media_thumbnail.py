# Generated by Django 4.1.13 on 2024-05-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_media_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]