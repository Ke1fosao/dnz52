from django.db import models
from ckeditor.fields import RichTextField
from gallery.models import GalleryAlbum


class SpecialistPage(models.Model):
    """Сторінка розділу спеціаліста (Методична, Фізкультурна тощо)"""

    PAGE_CHOICES = [
        ('methodical',   'Методична робота'),
        ('physical',     'Фізкультурно-оздоровча'),
        ('music',        'Музичний керівник'),
        ('psychologist', 'Психолог'),
        ('medical',      'Медична сестра'),
    ]

    page_type   = models.CharField('Тип сторінки', max_length=20,
                                   choices=PAGE_CHOICES, unique=True)
    title       = models.CharField('Заголовок сторінки', max_length=200)
    intro       = models.TextField('Вступний текст', blank=True,
                                   help_text='Короткий текст під заголовком')
    description = RichTextField('Опис діяльності (під картками спеціалістів)', blank=True,
                                 help_text='Розширений опис напрямку: програми, тема, методи роботи тощо.')
    theme_title = models.CharField('Заголовок науково-методичної теми', max_length=300, blank=True)
    theme_period = models.CharField('Період', max_length=50, blank=True,
                                     help_text='Наприклад: 2022–2027 роки')
    theme_text = models.TextField('Текст теми', blank=True)

    class Meta:
        verbose_name = 'Сторінка спеціаліста'
        verbose_name_plural = 'Сторінки спеціалістів'

    def __str__(self):
        return self.title


class Specialist(models.Model):
    """Спеціаліст (вихователь-методист, психолог тощо)"""

    page        = models.ForeignKey(SpecialistPage, on_delete=models.CASCADE,
                                    related_name='specialists',
                                    verbose_name='Сторінка')
    full_name   = models.CharField("ПІБ", max_length=200)
    position    = models.CharField('Посада', max_length=200)
    photo       = models.ImageField('Фото', upload_to='specialists/',
                                    blank=True, null=True)
    birth_date  = models.DateField('Дата народження', blank=True, null=True)
    education   = models.TextField('Освіта', blank=True)
    experience  = models.CharField('Педагогічний стаж', max_length=100, blank=True)
    category    = models.CharField('Кваліфікаційна категорія', max_length=100, blank=True)
    motto       = models.CharField('Життєве кредо / девіз', max_length=500, blank=True)
    bio         = RichTextField('Біографія / опис діяльності', blank=True)
    order       = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Спеціаліст'
        verbose_name_plural = 'Спеціалісти'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.full_name} — {self.page.title}'


class SpecialistAlbum(models.Model):
    """Фотоальбом на сторінці спеціаліста"""

    specialist  = models.ForeignKey(Specialist, on_delete=models.CASCADE,
                                    related_name='albums',
                                    verbose_name='Спеціаліст')
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE,
                                    verbose_name='Альбом')
    description = models.TextField('Опис заходу', blank=True)
    order       = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Альбом спеціаліста'
        verbose_name_plural = 'Альбоми спеціалістів'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.album.title} — {self.specialist.full_name}'


class SpecialistPageSection(models.Model):
    """Розділ сторінки спеціаліста (наприклад: «Зимові розваги», «День здоровʼя»).

    Тип `info` — показуємо опис + інлайн-галерею фото.
    Тип `event` — показуємо опис + кнопку-посилання на новину/альбом/зовнішнє посилання.
    """

    KIND_CHOICES = [
        ('info',  'Інформаційна (з інлайн-фото)'),
        ('event', 'Подія (посилання на альбом / новину)'),
    ]

    ACCENT_CHOICES = [
        ('primary',   'Синій'),
        ('success',   'Зелений'),
        ('warning',   'Помаранчевий'),
        ('danger',    'Червоний'),
        ('info',      'Бірюзовий'),
        ('purple',    'Фіолетовий'),
        ('pink',      'Рожевий'),
    ]

    page        = models.ForeignKey(SpecialistPage, on_delete=models.CASCADE,
                                     related_name='sections',
                                     verbose_name='Сторінка')
    title       = models.CharField('Заголовок розділу', max_length=200)
    subtitle    = models.CharField('Підзаголовок', max_length=300, blank=True)
    description = RichTextField('Опис розділу', blank=True)
    icon        = models.CharField('Іконка (Bootstrap Icons)', max_length=80,
                                    default='bi-lightning-fill',
                                    help_text='Наприклад: bi-snow, bi-sun, bi-bicycle, bi-heart-pulse.')
    accent      = models.CharField('Колір акценту', max_length=20,
                                    choices=ACCENT_CHOICES, default='primary')
    kind        = models.CharField('Тип розділу', max_length=10,
                                    choices=KIND_CHOICES, default='info')

    # Для типу «event» (заповнюйте лише ОДНЕ з полів):
    link_album   = models.ForeignKey(GalleryAlbum, on_delete=models.SET_NULL,
                                     blank=True, null=True,
                                     verbose_name='Альбом у галереї')
    link_news_slug = models.SlugField('Slug новини', blank=True,
                                       help_text='Slug існуючої новини (наприклад: svyato-oseni-u-zdo-52).')
    link_external_url = models.URLField('Зовнішнє посилання', blank=True)
    link_label   = models.CharField('Текст кнопки-посилання', max_length=100, blank=True,
                                     default='Переглянути фотоальбом')

    order       = models.IntegerField('Порядок', default=0)
    is_active   = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'Розділ сторінки спеціаліста'
        verbose_name_plural = 'Розділи сторінок спеціалістів'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.page.title} · {self.title}'

    def get_link_url(self):
        if self.link_album_id and self.link_album:
            from django.urls import reverse
            try:
                return reverse('gallery:album_detail', kwargs={'slug': self.link_album.slug})
            except Exception:
                return ''
        if self.link_news_slug:
            from django.urls import reverse
            try:
                return reverse('news:news_detail', kwargs={'slug': self.link_news_slug})
            except Exception:
                return ''
        if self.link_external_url:
            return self.link_external_url
        return ''

    @property
    def has_link(self):
        return bool(self.link_album_id or self.link_news_slug or self.link_external_url)


class SpecialistPagePhoto(models.Model):
    """Інлайн-фото для info-розділу сторінки спеціаліста."""

    section = models.ForeignKey(SpecialistPageSection, on_delete=models.CASCADE,
                                 related_name='photos',
                                 verbose_name='Розділ')
    image   = models.ImageField('Фото', upload_to='specialists/sections/')
    caption = models.CharField('Підпис', max_length=300, blank=True)
    order   = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Фото розділу спеціаліста'
        verbose_name_plural = 'Фото розділів спеціалістів'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.section.title} — {self.caption or f"Фото #{self.pk}"}'
