from django.db import models
from ckeditor.fields import RichTextField


class NewsCategory(models.Model):
    """Категорії новин"""
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Категорія новин'
        verbose_name_plural = 'Категорії новин'

    def __str__(self):
        return self.name


class News(models.Model):
    """Новини та оголошення"""
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категорія')
    content = RichTextField('Контент')
    image = models.ImageField('Зображення', upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField('Дата публікації', auto_now_add=True)
    updated_at = models.DateTimeField('Дата оновлення', auto_now=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    views = models.IntegerField('Перегляди', default=0)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
