from django.db import models
from gallery.models import GalleryAlbum


class Group(models.Model):
    """Група дітей"""
    AGE_CHOICES = [
        ('nursery',    'Ясельна (1.5–3 роки)'),
        ('junior',     'Молодша (3–4 роки)'),
        ('middle',     'Середня (4–5 років)'),
        ('senior',     'Старша (5–6 років)'),
        ('school',     'Підготовча (6–7 років)'),
    ]

    name        = models.CharField('Назва групи', max_length=200)
    slug        = models.SlugField('URL', unique=True)
    age_group   = models.CharField('Вікова категорія', max_length=20, choices=AGE_CHOICES, blank=True)
    motto       = models.CharField('Девіз групи', max_length=300, blank=True)
    description = models.TextField('Опис групи', blank=True)
    cover       = models.ImageField('Фото обкладинки', upload_to='groups/covers/', blank=True, null=True)
    color       = models.CharField('Колір групи (HEX)', max_length=7, default='#4A90E2',
                                   help_text='Наприклад: #FF6B6B')
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Фотоальбом групи')
    order       = models.IntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_teachers(self):
        return self.staff.filter(role='teacher')

    def get_assistants(self):
        return self.staff.filter(role='assistant')


class GroupStaff(models.Model):
    """Персонал групи (вихователі та помічники)"""
    ROLE_CHOICES = [
        ('teacher',   'Вихователь'),
        ('assistant', 'Помічник вихователя'),
    ]

    group       = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='staff',
                                    verbose_name='Група')
    role        = models.CharField('Посада', max_length=20, choices=ROLE_CHOICES, default='teacher')
    full_name   = models.CharField("Прізвище, ім'я, по батькові", max_length=200)
    photo       = models.ImageField('Фото', upload_to='groups/staff/', blank=True, null=True)
    birth_date  = models.DateField('Дата народження', blank=True, null=True)
    education   = models.TextField('Освіта', blank=True)
    experience  = models.CharField('Педагогічний стаж', max_length=100, blank=True)
    motto       = models.CharField('Життєве кредо', max_length=400, blank=True)
    order       = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Персонал групи'
        verbose_name_plural = 'Персонал груп'
        ordering = ['order', 'role']

    def __str__(self):
        return f'{self.full_name} ({self.get_role_display()}) — {self.group.name}'
