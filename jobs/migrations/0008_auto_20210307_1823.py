# Generated by Django 3.1.7 on 2021-03-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20210307_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]