# Generated by Django 4.2.6 on 2023-10-24 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ereading', '0002_alter_ereading_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ereading',
            name='user',
        ),
    ]
