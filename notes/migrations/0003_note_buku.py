# Generated by Django 4.2.4 on 2023-10-28 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_page', '0004_remove_komen_parent'),
        ('notes', '0002_rename_konten_catatan_note_isi_catatan'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='buku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_page.book'),
        ),
    ]