# Generated by Django 5.0.6 on 2024-05-15 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalusers', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/images.webp', null=True, upload_to='images/'),
        ),
    ]
