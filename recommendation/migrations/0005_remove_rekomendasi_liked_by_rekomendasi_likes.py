# Generated by Django 4.2.6 on 2023-10-29 11:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommendation', '0004_remove_rekomendasi_suka_buku_rekomendasi_liked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rekomendasi',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='rekomendasi',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]