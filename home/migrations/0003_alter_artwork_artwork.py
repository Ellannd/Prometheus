# Generated by Django 4.2.5 on 2024-01-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_artwork_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='artwork',
            field=models.ImageField(null=True, upload_to='artworks'),
        ),
    ]
