from django.db import models
from ckeditor.fields import RichTextField
from gallery.models import GalleryAlbum
from documents.models import Document


class Circle(models.Model):
    name        = models.CharField('Назва гуртка', max_length=200)
    slug        = models.SlugField('URL', unique=True)
    leader      = models.CharField('Керівник гуртка', max_length=200)
    age_group   = models.CharField('Вікова група', max_length=100, blank=True)
    schedule    = models.CharField('Розклад занять', max_length=200, blank=True)
    icon        = models.CharField('Іконка (Bootstrap Icons)', max_length=50, default='bi-star')
    color       = models.CharField('Колір (HEX)', max_length=7, default='#4A90E2')
    goal        = RichTextField('Мета та завдання')
    description = RichTextField('Опис діяльності')
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Фотоальбом')
    order       = models.IntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Гурток'
        verbose_name_plural = 'Гуртки'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class CircleDocument(models.Model):
    title    = models.CharField('Назва', max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='Документ')
    order    = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Документ гурткової роботи'
        verbose_name_plural = 'Документи гурткової роботи'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
