from django.db import migrations, models
import django.db.models.deletion
import ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialistPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('page_type', models.CharField(choices=[
                    ('methodical', 'Методична робота'),
                    ('physical', 'Фізкультурно-оздоровча'),
                    ('music', 'Музичний керівник'),
                    ('psychologist', 'Психолог'),
                    ('medical', 'Медична сестра'),
                ], max_length=20, unique=True, verbose_name='Тип сторінки')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок сторінки')),
                ('intro', models.TextField(blank=True, verbose_name='Вступний текст')),
            ],
            options={'verbose_name': 'Сторінка спеціаліста', 'verbose_name_plural': 'Сторінки спеціалістів'},
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=200, verbose_name='ПІБ')),
                ('position', models.CharField(max_length=200, verbose_name='Посада')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='specialists/', verbose_name='Фото')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата народження')),
                ('education', models.TextField(blank=True, verbose_name='Освіта')),
                ('experience', models.CharField(blank=True, max_length=100, verbose_name='Педагогічний стаж')),
                ('category', models.CharField(blank=True, max_length=100, verbose_name='Кваліфікаційна категорія')),
                ('motto', models.CharField(blank=True, max_length=500, verbose_name='Життєве кредо / девіз')),
                ('bio', ckeditor.fields.RichTextField(blank=True, verbose_name='Біографія / опис діяльності')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='specialists',
                                           to='specialists.specialistpage',
                                           verbose_name='Сторінка')),
            ],
            options={'verbose_name': 'Спеціаліст', 'verbose_name_plural': 'Спеціалісти', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='SpecialistAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, verbose_name='Опис заходу')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            to='gallery.galleryalbum',
                                            verbose_name='Альбом')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='albums',
                                                  to='specialists.specialist',
                                                  verbose_name='Спеціаліст')),
            ],
            options={'verbose_name': 'Альбом спеціаліста', 'verbose_name_plural': 'Альбоми спеціалістів', 'ordering': ['order', 'id']},
        ),
    ]
