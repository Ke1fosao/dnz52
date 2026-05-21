"""
Заповнюємо початкові дані для сторінки «Атестація»: 5 документів,
5 етапів, 4 категорії і 4 нормативних документи.
Так після деплою сторінка одразу виглядає повноцінно — а адмін може редагувати.
"""

from django.db import migrations


DOCUMENTS = [
    {
        'order': 1,
        'title': 'Наказ про створення атестаційної комісії І рівня ЗДО №52',
        'subtitle': 'Організація атестації педагогічних працівників у 2025–2026 навчальному році',
        'category': 'Наказ',
        'icon': 'bi-file-earmark-pdf-fill',
        'accent': 'primary',
        'url': 'https://drive.google.com/file/d/1_UUlNiLrYka4qqWjATmXEj8O5YFwo50L/view',
    },
    {
        'order': 2,
        'title': 'Графік засідань атестаційної комісії І рівня ЗДО №52',
        'subtitle': 'Розклад засідань на навчальний рік',
        'category': 'Графік',
        'icon': 'bi-calendar-event-fill',
        'accent': 'success',
        'url': 'https://drive.google.com/file/d/1lY5p1aZtg3AdWjhHlPpImuymbybu5USX/view',
    },
    {
        'order': 3,
        'title': 'Список педагогічних працівників, які підлягають черговій атестації у 2026 році',
        'subtitle': 'Фізкультурно-оздоровчий напрямок · Рівненська міська рада',
        'category': 'Список',
        'icon': 'bi-list-check',
        'accent': 'warning',
        'url': 'https://drive.google.com/file/d/1b_cEYsuuAi_A4Z_dUDN0Vzd6rpG8tjoa/view',
    },
    {
        'order': 4,
        'title': 'Строки проведення атестації педагогічних працівників',
        'subtitle': 'Фізкультурно-оздоровчий напрямок · Рівненська міська рада',
        'category': 'Строки',
        'icon': 'bi-clock-history',
        'accent': 'info',
        'url': 'https://drive.google.com/file/d/1Pc4iOsBqbkRIH9ValtWAiUHJFCR5BJyw/view',
    },
    {
        'order': 5,
        'title': 'Перелік документів для атестації педагогічних працівників',
        'subtitle': 'Що потрібно зібрати кожному педагогу',
        'category': 'Перелік',
        'icon': 'bi-file-earmark-text-fill',
        'accent': 'purple',
        'url': 'https://docs.google.com/document/d/1639okE18723j7yYSdK9rM7HtbcCqqZlD/edit',
    },
]


STEPS = [
    {
        'order': 1,
        'title': 'Подача заяви педагогічним працівником',
        'description': 'Не пізніше ніж за 3 місяці до планової дати атестації. '
                       'Заява подається на імʼя голови атестаційної комісії.',
    },
    {
        'order': 2,
        'title': 'Збір документів і характеристик',
        'description': 'Педагог готує портфоліо, методичні розробки, плани занять, '
                       'результати моніторингу професійної діяльності.',
    },
    {
        'order': 3,
        'title': 'Вивчення педагогічної діяльності',
        'description': 'Атестаційна комісія відвідує заняття, ознайомлюється з '
                       'документацією, проводить співбесіди з колегами.',
    },
    {
        'order': 4,
        'title': 'Засідання атестаційної комісії',
        'description': 'Розгляд матеріалів атестації за участі педагога згідно '
                       'з графіком засідань (див. документ №2).',
    },
    {
        'order': 5,
        'title': 'Ухвалення рішення',
        'description': 'Комісія приймає рішення про відповідність займаній посаді '
                       'та присвоєння (підтвердження) кваліфікаційної категорії.',
    },
]


CATEGORIES = [
    {
        'order': 1,
        'title': 'Спеціаліст',
        'description': 'Базовий рівень. Присвоюється на старті педагогічної діяльності.',
        'icon': 'bi-mortarboard',
        'color': 'cat-1',
    },
    {
        'order': 2,
        'title': 'Спеціаліст ІІ категорії',
        'description': 'Стаж від 3 років. Підтверджена професійна компетентність.',
        'icon': 'bi-bookmark-star',
        'color': 'cat-2',
    },
    {
        'order': 3,
        'title': 'Спеціаліст І категорії',
        'description': 'Стаж від 5 років. Високий рівень майстерності, методичний внесок.',
        'icon': 'bi-star-fill',
        'color': 'cat-3',
    },
    {
        'order': 4,
        'title': 'Спеціаліст вищої категорії',
        'description': 'Стаж від 8 років. Виняткова майстерність, наставництво колег.',
        'icon': 'bi-trophy-fill',
        'color': 'cat-4',
    },
]


LAWS = [
    {'order': 1, 'title': 'Закон України «Про освіту» (стаття 50)', 'url': ''},
    {'order': 2, 'title': 'Закон України «Про дошкільну освіту»', 'url': ''},
    {'order': 3, 'title': 'Типове положення про атестацію педагогічних працівників (наказ МОН України №805 від 09.09.2022)', 'url': ''},
    {'order': 4, 'title': 'Положення про сертифікацію педагогічних працівників', 'url': ''},
]


def seed_data(apps, schema_editor):
    AttestationDocument = apps.get_model('main', 'AttestationDocument')
    AttestationStep     = apps.get_model('main', 'AttestationStep')
    AttestationCategory = apps.get_model('main', 'AttestationCategory')
    AttestationLaw      = apps.get_model('main', 'AttestationLaw')
    AttestationSettings = apps.get_model('main', 'AttestationSettings')

    for data in DOCUMENTS:
        AttestationDocument.objects.get_or_create(title=data['title'], defaults=data)
    for data in STEPS:
        AttestationStep.objects.get_or_create(title=data['title'], defaults=data)
    for data in CATEGORIES:
        AttestationCategory.objects.get_or_create(title=data['title'], defaults=data)
    for data in LAWS:
        AttestationLaw.objects.get_or_create(title=data['title'], defaults=data)

    AttestationSettings.objects.get_or_create(pk=1)


def unseed_data(apps, schema_editor):
    """При відкаті — не чіпаємо дані (вони могли бути відредаговані адміном)."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_attestationcategory_attestationdocument_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]
