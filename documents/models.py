from django.db import models


class DocumentCategory(models.Model):
    """Категорії документів"""
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('URL', unique=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категорія документів'
        verbose_name_plural = 'Категорії документів'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Document(models.Model):
    """Документи для завантаження"""
    title = models.CharField('Назва документа', max_length=200)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категорія')
    file = models.FileField('Файл', upload_to='documents/')
    description = models.TextField('Опис', blank=True)
    created_at = models.DateTimeField('Дата додавання', auto_now_add=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    downloads = models.IntegerField('Завантажень', default=0)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_file_size(self):
        """Розмір файлу в МБ"""
        size = self.file.size / (1024 * 1024)
        return f'{size:.2f} МБ'
