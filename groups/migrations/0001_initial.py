from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва групи')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('age_group', models.CharField(blank=True, choices=[('nursery', 'Ясельна (1.5–3 роки)'), ('junior', 'Молодша (3–4 роки)'), ('middle', 'Середня (4–5 років)'), ('senior', 'Старша (5–6 років)'), ('school', 'Підготовча (6–7 років)')], max_length=20, verbose_name='Вікова категорія')),
                ('motto', models.CharField(blank=True, max_length=300, verbose_name='Девіз групи')),
                ('description', models.TextField(blank=True, verbose_name='Опис групи')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='groups/covers/', verbose_name='Фото обкладинки')),
                ('color', models.CharField(default='#4A90E2', help_text='Наприклад: #FF6B6B', max_length=7, verbose_name='Колір групи (HEX)')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубліковано')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gallery.galleryalbum', verbose_name='Фотоальбом групи')),
            ],
            options={
                'verbose_name': 'Група',
                'verbose_name_plural': 'Групи',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='GroupStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('teacher', 'Вихователь'), ('assistant', 'Помічник вихователя')], default='teacher', max_length=20, verbose_name='Посада')),
                ('full_name', models.CharField(max_length=200, verbose_name="Прізвище, ім'я, по батькові")),
                ('photo', models.ImageField(blank=True, null=True, upload_to='groups/staff/', verbose_name='Фото')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата народження')),
                ('education', models.TextField(blank=True, verbose_name='Освіта')),
                ('experience', models.CharField(blank=True, max_length=100, verbose_name='Педагогічний стаж')),
                ('motto', models.CharField(blank=True, max_length=400, verbose_name='Життєве кредо')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='groups.group', verbose_name='Група')),
            ],
            options={
                'verbose_name': 'Персонал групи',
                'verbose_name_plural': 'Персонал груп',
                'ordering': ['order', 'role'],
            },
        ),
    ]
