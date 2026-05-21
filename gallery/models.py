from django.db import models


class GalleryCategory(models.Model):
    """Категорії фотоальбомів — щоб згрупувати галереї груп / свят / занять."""
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('URL', unique=True)
    icon = models.CharField(
        'Іконка (Bootstrap Icons)', max_length=80, default='bi-folder-fill',
        blank=True,
        help_text='Назва класу з Bootstrap Icons, наприклад: bi-people-fill, bi-balloon-fill.'
    )
    color = models.CharField(
        'Колір (HEX)', max_length=7, default='#4A90E2', blank=True,
        help_text='Колір заголовка секції на сторінці галереї. Наприклад: #4A90E2.'
    )
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категорія альбомів'
        verbose_name_plural = 'Категорії альбомів'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class GalleryAlbum(models.Model):
    """Альбоми фотогалереї"""
    title = models.CharField('Назва альбому', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Опис', blank=True)
    cover = models.ImageField('Обкладинка', upload_to='gallery/covers/')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='albums',
        verbose_name='Категорія',
        help_text='Виберіть розділ галереї, де показуватиметься альбом '
                  '(якщо порожньо — показуватиметься у блоці «Інше»).'
    )
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
