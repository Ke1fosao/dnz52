"""
Кастомізація бічного списку розділів у Django-адмінці для ЗДО №52.

Стандартна адмінка показує моделі згруповані за технічними назвами apps
(MAIN, NEWS, GALLERY...). Для людей, які вперше відкривають адмінку,
це виглядає страшно. Тут ми перегруповуємо моделі у логічні розділи з
емодзі і зрозумілими українськими назвами.
"""

import types


# Структура: список «секцій», кожна — як «папка» з кількома моделями.
# Кортеж (app_label, ModelName, custom_label_або_None).
# Якщо custom_label = None — лишається оригінальне verbose_name_plural моделі.
SECTIONS = [
    {
        'name': '📰 Новини',
        'description': 'Додавання та редагування новин закладу',
        'models': [
            ('news', 'News',         'Новини'),
            ('news', 'NewsCategory', 'Категорії новин'),
        ],
    },
    {
        'name': '🖼️ Фотогалерея',
        'description': 'Альбоми і фото для розділу «Галерея»',
        'models': [
            ('gallery', 'GalleryAlbum',    'Альбоми'),
            ('gallery', 'GalleryCategory', 'Категорії альбомів'),
            ('gallery', 'GalleryPhoto',    'Окремі фото'),
        ],
    },
    {
        'name': '💬 Відгуки',
        'description': 'Модерація відгуків від батьків',
        'models': [
            ('reviews', 'Review', 'Відгуки батьків'),
        ],
    },
    {
        'name': '🏘️ Групи дитячого садка',
        'description': 'Інформація про групи №1–14 та персонал',
        'models': [
            ('groups', 'Group',      'Групи'),
            ('groups', 'GroupStaff', 'Працівники груп'),
        ],
    },
    {
        'name': '🎨 Гурткова робота',
        'description': 'Гуртки, секції та документи з організації',
        'models': [
            ('circles', 'Circle',         'Гуртки'),
            ('circles', 'CircleDocument', 'Документи гурткової роботи'),
        ],
    },
    {
        'name': '👩‍🏫 Спеціалісти (методичні сторінки)',
        'description': 'Сторінки методиста, психолога, фізкультурного та інших',
        'models': [
            ('specialists', 'Specialist',            'Спеціалісти'),
            ('specialists', 'SpecialistPage',        'Сторінки спеціалістів'),
            ('specialists', 'SpecialistPageSection', 'Тематичні розділи сторінок'),
        ],
    },
    {
        'name': '🏠 Головна сторінка',
        'description': 'Слайдер та контакти на головній',
        'models': [
            ('main', 'Slider',  'Слайди вгорі сайту'),
            ('main', 'Contact', 'Контактна інформація'),
        ],
    },
    {
        'name': '📄 Інформаційні сторінки',
        'description': 'Про заклад, Історія, Правила тощо',
        'models': [
            ('main', 'Page', 'Усі сторінки'),
        ],
    },
    {
        'name': '👨‍👩‍👧 Батьківська сторінка',
        'description': 'Все що бачать батьки на сторінці «Батькам»',
        'models': [
            ('main', 'ParentsAnnouncement',      '01 — Оголошення (банер)'),
            ('main', 'ParentsDocument',          '02 — Корисні документи / посилання'),
            ('main', 'ParentsAdaptationPhoto',   '03 — Фото порад про адаптацію'),
            ('main', 'ParentsEnrollmentDoc',     '04 — Документи для зарахування'),
            ('main', 'ParentsApplicationSample', '05 — Зразки заяв'),
        ],
    },
    {
        'name': '🎓 Керівництво закладу',
        'description': 'Директор, методист, адміністрація',
        'models': [
            ('main', 'StaffMember', 'Працівники адміністрації'),
        ],
    },
    {
        'name': '📜 Атестація педагогів',
        'description': 'Документи та інформація про атестаційну комісію',
        'models': [
            ('main', 'AttestationSettings', '00 — Тексти на сторінці'),
            ('main', 'AttestationDocument', '01 — Документи атестаційної комісії'),
            ('main', 'AttestationStep',     '02 — Етапи атестації'),
            ('main', 'AttestationCategory', '03 — Кваліфікаційні категорії'),
            ('main', 'AttestationLaw',      '04 — Нормативна база'),
        ],
    },
    {
        'name': '📁 Документи (загальний розділ)',
        'description': 'Сторінка /documents/ — нормативка, накази, звіти',
        'models': [
            ('documents', 'Document',         'Документи'),
            ('documents', 'DocumentCategory', 'Категорії документів'),
        ],
    },
]


def customize_app_list(site):
    """Замінює бічний список розділів адмінки на наш — згрупований і красивий."""
    original_get_app_list = site.get_app_list

    def new_get_app_list(self, request, app_label=None):
        # Стандартний список як його генерує Django
        app_list = original_get_app_list(request, app_label)

        # Зробимо швидкий пошук: (app_label, ModelName) → model_dict
        model_map = {}
        for app in app_list:
            for model in app['models']:
                key = (app['app_label'], model['object_name'])
                model_map[key] = model

        # Будуємо новий список у нашому порядку
        new_list = []
        used = set()
        for section in SECTIONS:
            section_models = []
            for app_lbl, model_name, custom_name in section['models']:
                key = (app_lbl, model_name)
                if key not in model_map:
                    continue  # модель не існує або користувач не має прав
                model = dict(model_map[key])
                if custom_name:
                    model['name'] = custom_name
                section_models.append(model)
                used.add(key)

            if section_models:
                new_list.append({
                    'name':            section['name'],
                    'app_label':       section.get('label', 'dnz_' + section['name'][:8]),
                    'app_url':         section_models[0].get('admin_url', ''),
                    'has_module_perms': True,
                    'models':          section_models,
                    # Опис не показується у стандартній бічці, але рендериться у нашому welcome
                    'dnz_description': section.get('description', ''),
                })

        # Усе що не вписалося у наші секції — кидаємо в «Системне» (наприклад users, groups Django)
        leftovers = []
        for app in app_list:
            for model in app['models']:
                key = (app['app_label'], model['object_name'])
                if key not in used:
                    leftovers.append(model)
        if leftovers:
            new_list.append({
                'name':            '⚙️ Системне (користувачі і доступи)',
                'app_label':       'system',
                'app_url':         '/admin/auth/',
                'has_module_perms': True,
                'models':          leftovers,
                'dnz_description': 'Технічна частина — змінювати лише за потреби',
            })

        return new_list

    # Прив'язуємо як метод сайту
    site.get_app_list = types.MethodType(new_get_app_list, site)
