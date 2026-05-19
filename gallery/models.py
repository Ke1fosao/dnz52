from django.db import models


class GalleryAlbum(models.Model):
    """Альбоми фотогалереї"""
    title = models.CharField('Назва альбому', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Опис', blank=True)
    cover = models.ImageField('Обкладинка', upload_to='gallery/covers/')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбоми'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    """Фотографії в альбомах"""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos', verbose_name='Альбом')
    image = models.ImageField('Фото', upload_to='gallery/photos/')
    title = models.CharField('Назва', max_length=200, blank=True)
    description = models.TextField('Опис', blank=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографії'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f'Фото {self.id}'
