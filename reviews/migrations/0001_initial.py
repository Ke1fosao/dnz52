from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Review', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('author', models.CharField(max_length=100, verbose_name="Ім'я")),
            ('child_group', models.CharField(blank=True, max_length=100, verbose_name='Група дитини')),
            ('rating', models.IntegerField(choices=[(1,'★'),(2,'★★'),(3,'★★★'),(4,'★★★★'),(5,'★★★★★')], default=5, verbose_name='Оцінка')),
            ('text', models.TextField(verbose_name='Відгук')),
            ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ('is_approved', models.BooleanField(default=False, verbose_name='Опубліковано')),
        ], options={'verbose_name': 'Відгук', 'verbose_name_plural': 'Відгуки', 'ordering': ['-created_at']}),
    ]
