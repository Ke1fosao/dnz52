from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Page(models.Model):
    """Статичні сторінки (Про заклад, Контакти тощо)"""
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    content = RichTextField('Контент')
    image = models.ImageField('Зображення', upload_to='pages/', blank=True, null=True)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('Дата оновлення', auto_now=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Сторінка'
        verbose_name_plural = 'Сторінки'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class PageImage(models.Model):
    """Додаткові зображення/фото для сторінки (показуються галереєю)."""
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='images',
        verbose_name='Сторінка',
    )
    image = models.ImageField('Зображення', upload_to='pages/gallery/')
    caption = models.CharField('Підпис', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Зображення сторінки'
        verbose_name_plural = 'Зображення сторінок'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.page.title} — {self.caption or f"Зображення #{self.pk}"}'


class Slider(models.Model):
    """Слайдер на головній сторінці"""
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='slider/')
    link = models.CharField('Посилання', max_length=200, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'
        ordering = ['order']

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Контактна інформація"""
    address = models.CharField('Адреса', max_length=300)
    phone = models.CharField('Телефон', max_length=100)
    email = models.EmailField('Email')
    working_hours = models.TextField('Режим роботи')
    map_embed = models.TextField('Код карти Google Maps', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'

    def __str__(self):
        return 'Контактна інформація'


# ============================================================================
# Батьківська сторінка — секції контенту, які редагуються через адмінку
# ============================================================================

class ParentsAnnouncement(models.Model):
    """Оголошення-банер на батьківській сторінці (зверху сторінки)."""
    title = models.CharField('Заголовок', max_length=200, blank=True,
                              help_text='Підпис під зображенням. Можна залишити порожнім.')
    image = models.ImageField('Зображення', upload_to='parents/announcements/')
    link = models.URLField('Посилання (за бажанням)', blank=True,
                            help_text='Якщо вказано — зображення буде клікабельне.')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = '01. Оголошення (батькам)'
        verbose_name_plural = '01. Оголошення (батькам)'
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f'Оголошення #{self.pk}'


class ParentsDocument(models.Model):
    """Документ/посилання на батьківській сторінці (Памятка, Правила, Положення тощо)."""
    LINK_TYPE_CHOICES = [
        ('external', 'Зовнішнє посилання (URL)'),
        ('page', 'Внутрішня сторінка (slug)'),
        ('file', 'Файл для завантаження'),
    ]
    title = models.CharField('Назва', max_length=300)
    description = models.CharField('Короткий опис', max_length=500, blank=True)
    link_type = models.CharField('Тип посилання', max_length=20, choices=LINK_TYPE_CHOICES, default='external')
    external_url = models.URLField('Зовнішня URL-адреса', blank=True,
                                    help_text='Заповнюйте, якщо тип = "Зовнішнє посилання".')
    internal_slug = models.SlugField('Slug сторінки', blank=True,
                                      help_text='Slug внутрішньої сторінки (Page). Заповнюйте, якщо тип = "Внутрішня сторінка".')
    file = models.FileField('Файл', upload_to='parents/documents/', blank=True, null=True,
                             help_text='Завантажуйте, якщо тип = "Файл".')
    icon = models.CharField('Іконка (Bootstrap Icons)', max_length=80, default='bi-file-earmark-pdf',
                              help_text='Назва класу Bootstrap Icon, наприклад: bi-file-earmark-pdf, bi-shield-check.')
    accent = models.CharField('Колір акценту', max_length=20, default='primary',
                                help_text='primary, success, warning, danger, info, secondary')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '02. Документ (батькам)'
        verbose_name_plural = '02. Документи (батькам)'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.link_type == 'external' and self.external_url:
            return self.external_url
        if self.link_type == 'page' and self.internal_slug:
            try:
                return reverse('main:page_detail', kwargs={'slug': self.internal_slug})
            except Exception:
                return '#'
        if self.link_type == 'file' and self.file:
            return self.file.url
        return '#'

    @property
    def is_external(self):
        return self.link_type == 'external'


class ParentsAdaptationPhoto(models.Model):
    """Фото для блоку "Поради щодо адаптації дітей"."""
    title = models.CharField('Підпис (необов\'язково)', max_length=200, blank=True)
    image = models.ImageField('Фото', upload_to='parents/adaptation/')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = '03. Фото адаптації'
        verbose_name_plural = '03. Фото адаптації'
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f'Фото адаптації #{self.pk}'


class ParentsEnrollmentDoc(models.Model):
    """Перелік документів для зарахування дитини до ЗДО."""
    title = models.CharField('Назва документа', max_length=300)
    note = models.CharField('Примітка', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '04. Документ для зарахування'
        verbose_name_plural = '04. Документи для зарахування'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class ParentsApplicationSample(models.Model):
    """Зразок заяви для зарахування (фото/скан)."""
    title = models.CharField('Заголовок', max_length=200, default='Зразок заяви')
    image = models.ImageField('Фото зразка', upload_to='parents/samples/')
    caption = models.CharField('Підпис під фото', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '05. Зразок заяви'
        verbose_name_plural = '05. Зразки заяв'
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f'Зразок заяви #{self.pk}'


# ============================================================================
# Керівництво / Адміністрація закладу
# ============================================================================

# ============================================================================
# Сторінка «Атестація педагогічних працівників»
# ============================================================================

ACCENT_CHOICES = [
    ('primary', 'Синій'),
    ('success', 'Зелений'),
    ('warning', 'Помаранчевий'),
    ('info',    'Блакитний'),
    ('purple',  'Фіолетовий'),
    ('danger',  'Червоний'),
]


class AttestationDocument(models.Model):
    """Документ атестаційної комісії (наказ, графік, список тощо) — посилання на файл."""
    title = models.CharField('Назва документа', max_length=400)
    subtitle = models.CharField('Короткий опис / уточнення', max_length=300, blank=True)
    category = models.CharField('Тип документа', max_length=50, default='Документ',
                                  help_text='Коротка мітка: Наказ, Графік, Список, Строки, Перелік тощо.')
    url = models.URLField('Посилання на документ',
                            help_text='URL у Google Drive / Docs або на ваш сайт.')
    icon = models.CharField('Іконка (Bootstrap Icons)', max_length=80,
                              default='bi-file-earmark-pdf-fill',
                              help_text='Наприклад: bi-file-earmark-pdf-fill, bi-calendar-event-fill.')
    accent = models.CharField('Колір акценту', max_length=20, choices=ACCENT_CHOICES, default='primary')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '01. Документ атестації'
        verbose_name_plural = '01. Документи атестаційної комісії'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class AttestationStep(models.Model):
    """Етап проведення атестації — нумерований крок."""
    title = models.CharField('Назва етапу', max_length=300)
    description = models.TextField('Пояснення', blank=True)
    order = models.IntegerField('Порядок (= номер кроку)', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '02. Етап атестації'
        verbose_name_plural = '02. Етапи проведення атестації'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class AttestationCategory(models.Model):
    """Кваліфікаційна категорія педагога."""
    COLOR_CHOICES = [
        ('cat-1', '🟢 Зелений (Спеціаліст)'),
        ('cat-2', '🔵 Блакитний (II категорія)'),
        ('cat-3', '🔷 Синій (I категорія)'),
        ('cat-4', '🟣 Фіолетовий (Вища)'),
    ]
    title = models.CharField('Назва категорії', max_length=200)
    description = models.TextField('Опис / вимоги',
                                     help_text='Стисло: умови присвоєння, стаж тощо.')
    icon = models.CharField('Іконка (Bootstrap Icons)', max_length=80, default='bi-mortarboard',
                              help_text='Наприклад: bi-mortarboard, bi-star-fill, bi-trophy-fill.')
    color = models.CharField('Колір', max_length=10, choices=COLOR_CHOICES, default='cat-1')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '03. Кваліфікаційна категорія'
        verbose_name_plural = '03. Кваліфікаційні категорії'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class AttestationLaw(models.Model):
    """Нормативний документ, що регулює атестацію."""
    title = models.CharField('Назва нормативного документа', max_length=400)
    url = models.URLField('Посилання (необовʼязкове)', blank=True,
                            help_text='Якщо є — назва стане клікабельною.')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = '04. Нормативний документ'
        verbose_name_plural = '04. Нормативна база атестації'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class AttestationSettings(models.Model):
    """Загальні налаштування сторінки атестації (текст hero, інтро, контактна підказка)."""
    hero_lead = models.TextField('Підзаголовок під H1 (hero)',
                                    default='Атестація — це система заходів, спрямована на всебічне комплексне '
                                            'оцінювання педагогічної діяльності, за результатами якої '
                                            'присвоюється кваліфікаційна категорія.')
    intro_html = RichTextField('Вступний блок (синій, ліворуч)',
                                  help_text='Підтримує форматування. Зʼявляється угорі сторінки.',
                                  blank=True)
    docs_section_subtitle = models.CharField('Підзаголовок секції документів', max_length=200,
                                               default='2025–2026 навчальний рік')
    contact_title = models.CharField('Заголовок підказки про контакти', max_length=200,
                                       default='Маєте запитання щодо атестації?')
    contact_html = RichTextField('Текст підказки про контакти (жовтий блок)',
                                    default='<p>Звертайтеся до <strong>вихователя-методиста</strong> закладу — '
                                            'він допоможе з оформленням документів, поясненням етапів і термінів.</p>',
                                    blank=True)

    class Meta:
        verbose_name = '00. Налаштування сторінки'
        verbose_name_plural = '00. Налаштування сторінки атестації'

    def __str__(self):
        return 'Налаштування сторінки «Атестація»'

    @classmethod
    def get_solo(cls):
        """Повертає єдиний запис налаштувань, створюючи його за потреби."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class StaffMember(models.Model):
    """Член керівництва/адміністрації закладу — для сторінки «Керівництво»."""
    full_name = models.CharField('Прізвище, імʼя, по батькові', max_length=200)
    position = models.CharField('Посада', max_length=200)
    photo = models.ImageField('Фото', upload_to='staff/', blank=True, null=True,
                                help_text='Якщо порожньо — використовується аватар-плейсхолдер.')
    education = models.CharField('Освіта', max_length=300, blank=True,
                                  help_text='Наприклад: вища; вища, спеціаліст вищої категорії.')
    experience = models.CharField('Стаж', max_length=200, blank=True,
                                   help_text='Наприклад: стаж педагогічної роботи 36 років.')
    category = models.CharField('Категорія / Звання', max_length=300, blank=True)
    awards = models.TextField('Нагороди та звання', blank=True,
                                help_text='Кожна нагорода — з нового рядка. Будуть показані як список.')
    bio = RichTextField('Біографія / Додаткова інформація', blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    reception_hours = models.CharField('Години прийому', max_length=200, blank=True)
    is_featured = models.BooleanField('Виділити (директор/головна особа)', default=False,
                                       help_text='Виділена картка показується першою у великому форматі.')
    accent_color = models.CharField('Колір акценту', max_length=20, default='primary',
                                      help_text='primary, success, warning, danger, info, purple')
    detail_url = models.CharField('Посилання на повну сторінку', max_length=300, blank=True,
                                   help_text='Наприклад: /specialists/psychologist/ або /specialists/medical/')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'Член керівництва'
        verbose_name_plural = 'Керівництво / Адміністрація'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.full_name} — {self.position}'

    @property
    def awards_list(self):
        """Повертає список нагород рядок-за-рядком."""
        if not self.awards:
            return []
        return [a.strip() for a in self.awards.splitlines() if a.strip()]
