# Generated by Django 4.1.13 on 2024-05-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_media_url_media_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='version',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]