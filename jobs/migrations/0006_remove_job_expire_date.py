# Generated by Django 3.1.7 on 2021-03-07 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_expire_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='expire_date',
        ),
    ]