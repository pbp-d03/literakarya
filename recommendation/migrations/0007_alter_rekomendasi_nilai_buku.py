# Generated by Django 4.2.6 on 2023-10-29 14:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0006_alter_rekomendasi_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rekomendasi',
            name='nilai_buku',
            field=models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]