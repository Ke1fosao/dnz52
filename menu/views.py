from datetime import date, timedelta
from django.shortcuts import render
from .models import DailyMenu


_WEEKDAYS_UK_FULL = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя']
_WEEKDAYS_UK_SHORT = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']


def _parse_iso_date(s):
    """Парсимо рядок YYYY-MM-DD. Якщо невалідно — повертаємо None."""
    if not s:
        return None
    try:
        return date.fromisoformat(s.strip())
    except (ValueError, TypeError, AttributeError):
        return None


def _week_range(ref_date):
    """Повертає (понеділок, неділя) тижня, у який потрапляє ref_date."""
    monday = ref_date - timedelta(days=ref_date.weekday())
    return monday, monday + timedelta(days=6)


def menu_page(request):
    """Сторінка «Меню харчування» — показує сьогоднішнє меню + поточний тиждень.
       Підтримує навігацію через ?date=YYYY-MM-DD."""
    today = date.today()
    ref_date = _parse_iso_date(request.GET.get('date')) or today

    week_start, week_end = _week_range(ref_date)
    week_dates = [week_start + timedelta(days=i) for i in range(7)]

    # Завантажуємо всі опубліковані меню тижня одним запитом
    week_menus = {
        m.date: m
        for m in DailyMenu.objects.filter(date__in=week_dates, is_published=True)
    }

    days = []
    for i, d in enumerate(week_dates):
        days.append({
            'date':            d,
            'weekday':         _WEEKDAYS_UK_FULL[i],
            'weekday_short':   _WEEKDAYS_UK_SHORT[i],
            'is_today':        d == today,
            'is_past':         d < today,
            'is_weekend':      i >= 5,
            'menu':            week_menus.get(d),
        })

    # Сьогоднішнє меню (як окрема «головна» картка)
    today_menu = DailyMenu.objects.filter(date=today, is_published=True).first()

    # Чи це поточний тиждень?
    is_current_week = week_start <= today <= week_end

    return render(request, 'menu/menu_page.html', {
        'today':           today,
        'today_menu':      today_menu,
        'reference_date':  ref_date,
        'week_start':      week_start,
        'week_end':        week_end,
        'days':            days,
        'prev_week_date':  (week_start - timedelta(days=7)).isoformat(),
        'next_week_date':  (week_start + timedelta(days=7)).isoformat(),
        'today_iso':       today.isoformat(),
        'is_current_week': is_current_week,
    })
