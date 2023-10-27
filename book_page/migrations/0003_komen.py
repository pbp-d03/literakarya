from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book_page', '0002_auto_20231021_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='Komen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isi_komen', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
                ('buku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_page.book')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balasan', to='book_page.komen')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
