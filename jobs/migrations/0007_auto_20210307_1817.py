# Generated by Django 3.1.7 on 2021-03-07 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_remove_job_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
