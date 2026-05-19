from django.db import migrations, models
import django.db.models.deletion
import ckeditor.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [('gallery', '0001_initial'), ('documents', '0001_initial')]
    operations = [
        migrations.CreateModel(name='Circle', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('name', models.CharField(max_length=200, verbose_name='Назва гуртка')),
            ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ('leader', models.CharField(max_length=200, verbose_name='Керівник')),
            ('age_group', models.CharField(blank=True, max_length=100, verbose_name='Вікова група')),
            ('schedule', models.CharField(blank=True, max_length=200, verbose_name='Розклад')),
            ('icon', models.CharField(default='bi-star', max_length=50, verbose_name='Іконка')),
            ('color', models.CharField(default='#4A90E2', max_length=7, verbose_name='Колір')),
            ('goal', ckeditor.fields.RichTextField(verbose_name='Мета та завдання')),
            ('description', ckeditor.fields.RichTextField(verbose_name='Опис діяльності')),
            ('order', models.IntegerField(default=0, verbose_name='Порядок')),
            ('is_published', models.BooleanField(default=True, verbose_name='Опубліковано')),
            ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gallery.galleryalbum', verbose_name='Фотоальбом')),
        ], options={'verbose_name': 'Гурток', 'verbose_name_plural': 'Гуртки', 'ordering': ['order', 'name']}),
        migrations.CreateModel(name='CircleDocument', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('title', models.CharField(max_length=200, verbose_name='Назва')),
            ('order', models.IntegerField(default=0, verbose_name='Порядок')),
            ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document', verbose_name='Документ')),
        ], options={'verbose_name': 'Документ гуртку', 'verbose_name_plural': 'Документи гуртків', 'ordering': ['order', 'id']}),
    ]
