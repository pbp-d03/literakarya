# Generated by Django 4.2.6 on 2023-10-25 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_post_user_reply_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='topic',
            new_name='post',
        ),
    ]