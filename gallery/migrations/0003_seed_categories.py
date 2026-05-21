"""Початкові категорії для фотогалереї — щоб одразу після деплою було куди класти альбоми."""

from django.db import migrations


CATEGORIES = [
    {
        'name':  'Групи дитячого садка',
        'slug':  'groups',
        'icon':  'bi-people-fill',
        'color': '#4A90E2',
        'order': 1,
    },
    {
        'name':  'Свята та події',
        'slug':  'events',
        'icon':  'bi-balloon-fill',
        'color': '#FF8FA3',
        'order': 2,
    },
    {
        'name':  'Заняття та проєкти',
        'slug':  'activities',
        'icon':  'bi-easel2-fill',
        'color': '#50E3C2',
        'order': 3,
    },
    {
        'name':  'Літня кампанія',
        'slug':  'summer',
        'icon':  'bi-sun-fill',
        'color': '#FFB84D',
        'order': 4,
    },
    {
        'name':  'Спортивні заходи',
        'slug':  'sports',
        'icon':  'bi-trophy-fill',
        'color': '#38C2DD',
        'order': 5,
    },
    {
        'name':  'Інше',
        'slug':  'other',
        'icon':  'bi-folder-fill',
        'color': '#7B8AA5',
        'order': 99,
    },
]


def seed(apps, schema_editor):
    GalleryCategory = apps.get_model('gallery', 'GalleryCategory')
    for data in CATEGORIES:
        GalleryCategory.objects.get_or_create(slug=data['slug'], defaults=data)


def unseed(apps, schema_editor):
    """При відкаті не чіпаємо — могли бути ручні зміни адміна."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_gallerycategory_galleryalbum_category'),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
