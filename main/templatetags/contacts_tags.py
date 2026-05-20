"""
Допоміжні фільтри/теги для шаблону Контактів.

Робимо так, щоб шаблон вмів «зрозуміти» неідеальні дані з адмінки:
    - телефони, введені через кому або з нового рядка
    - режим роботи у вигляді стіни тексту через крапку з комою
    - map_embed з простою URL замість iframe
"""

import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


# ---------------------------------------------------------------------------
# Телефони
# ---------------------------------------------------------------------------

@register.filter
def split_phones(value):
    """
    Розбиває рядок з телефонами на список окремих номерів.
    Підтримує розділювачі: переноси рядка, крапка з комою, кома, символ '/'.
    Прибирає кінцеву крапку, пробіли і дужки.
    """
    if not value:
        return []
    raw_parts = re.split(r'[\n;,/]+', str(value))
    result = []
    for part in raw_parts:
        cleaned = part.strip().rstrip('.').strip()
        if cleaned:
            result.append(cleaned)
    return result


@register.filter
def tel_link(phone):
    """
    Перетворює відображуваний телефон у безпечне tel:-посилання.
    Залишає тільки цифри, '+' на початку — все інше прибирає.
    Наприклад: "(0362) 64-82-55" → "tel:+380362648255" (якщо
    помітимо, що без +380 — додаємо), або "64-82-55" → "tel:648255".
    """
    if not phone:
        return ''
    digits = re.sub(r'[^\d+]', '', str(phone))
    # Якщо номер починається з '0' (типовий український формат) і не має '+',
    # підставляємо префікс +38.
    if digits.startswith('0') and not digits.startswith('+'):
        digits = '+38' + digits
    return f'tel:{digits}'


# ---------------------------------------------------------------------------
# Режим роботи
# ---------------------------------------------------------------------------

@register.filter
def split_hours(value):
    """
    Розбиває рядок з режимом роботи на акуратний список пунктів.
    Підтримує розділювачі: ';', переноси рядка.
    """
    if not value:
        return []
    raw_parts = re.split(r'[\n;]+', str(value))
    return [p.strip().rstrip('.,').strip() for p in raw_parts if p.strip()]


# ---------------------------------------------------------------------------
# Map embed
# ---------------------------------------------------------------------------

# Регулярка для розпізнавання гугл-мапсівського посилання
_MAP_URL_RE = re.compile(r'^https?://[^\s"]+', re.IGNORECASE)


@register.simple_tag
def render_map_embed(map_embed):
    """
    Розумно відображає вміст поля Contact.map_embed:
        - якщо це <iframe ...> з повним кодом — повертає як є
        - якщо це посилання на Google Maps — обгортає у <iframe>
        - якщо порожньо — повертає порожній рядок (шаблон сам покаже плейсхолдер)
    """
    if not map_embed:
        return ''

    raw = str(map_embed).strip()
    lowered = raw.lower()

    # Випадок 1 — повний iframe код, вже готовий до використання
    if '<iframe' in lowered:
        return mark_safe(raw)

    # Випадок 2 — голий URL, нам треба зробити з нього вбудовану карту
    if _MAP_URL_RE.match(raw):
        url = raw
        # Якщо це звичайне посилання на /maps?q=... — додаємо &output=embed
        if 'output=embed' not in url and '/maps/embed' not in url:
            sep = '&' if '?' in url else '?'
            url = f'{url}{sep}output=embed'
        # Безпечне екранування URL у атрибуті
        return mark_safe(
            f'<iframe src="{escape(url)}" '
            f'width="100%" height="420" style="border:0;" '
            f'loading="lazy" allowfullscreen '
            f'referrerpolicy="no-referrer-when-downgrade"></iframe>'
        )

    # Випадок 3 — щось дивне, нерозпізнане. Не показуємо нічого.
    return ''


# ---------------------------------------------------------------------------
# Адреса — невелика красива розбивка на «індекс + місто» і «вулиця»
# ---------------------------------------------------------------------------

@register.filter
def address_lines(value):
    """
    Намагається розбити адресу на 2 змістовні рядки:
        - перший рядок: індекс + місто
        - другий рядок: вулиця, будинок
    Якщо парс не вдався — повертаємо однорядковий список з оригіналом.

    Приклад:
        "33016 м.Рівне вул.Коновальця, 17-б."
        → ["33016 м.Рівне", "вул.Коновальця, 17-б."]
    """
    if not value:
        return []
    raw = str(value).strip().rstrip('.').strip()

    # Спочатку — якщо адреса вже на кількох рядках, повертаємо як є.
    if '\n' in raw:
        return [line.strip().rstrip(',').strip() for line in raw.splitlines() if line.strip()]

    # Шукаємо точку розділу: ключове слово «вул.», «провулок», «бульвар» тощо
    m = re.search(r'\b(вул\.|вулиця|пров\.|провулок|просп\.|проспект|бульв\.|бульвар|пл\.|площа)', raw, re.IGNORECASE)
    if m:
        first = raw[:m.start()].strip().rstrip(',').strip()
        second = raw[m.start():].strip().rstrip(',').strip()
        if first and second:
            return [first, second]

    return [raw]
