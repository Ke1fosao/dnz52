import time
from django.shortcuts import render
from django.db.models import Avg
from .models import Review


SORT_ORDERS = {
    'newest':  ('-created_at',),
    'oldest':  ('created_at',),
    'highest': ('-rating', '-created_at'),
    'lowest':  ('rating', '-created_at'),
}

# Мінімальний інтервал між відгуками з однієї сесії (захист від спаму)
REVIEW_COOLDOWN_SECONDS = 60


def reviews_page(request):
    """Сторінка відгуків з фільтрацією за оцінкою та сортуванням."""
    base_qs = Review.objects.filter(is_approved=True)
    submitted = False
    spam_blocked = False
    cooldown_blocked = False

    if request.method == 'POST':
        # === ЗАХИСТ №1: HONEYPOT ===
        # Приховане поле "website" не бачить людина (display:none у формі),
        # але бот, який автоматично заповнює всі поля — заповнить.
        # Якщо поле не порожнє — це бот, тихо «приймаємо» але нічого не зберігаємо.
        honeypot = request.POST.get('website', '').strip()
        if honeypot:
            spam_blocked = True

        # === ЗАХИСТ №2: RATE-LIMIT ===
        # Не дозволяємо лишати > 1 відгук за 60 сек з однієї сесії.
        last_ts = request.session.get('last_review_ts', 0)
        now_ts = int(time.time())
        if not spam_blocked and now_ts - last_ts < REVIEW_COOLDOWN_SECONDS:
            cooldown_blocked = True

        author      = request.POST.get('author', '').strip()[:100]
        child_group = request.POST.get('child_group', '').strip()[:100]
        try:
            rating = int(request.POST.get('rating', 5) or 5)
        except (TypeError, ValueError):
            rating = 5
        rating = max(1, min(5, rating))  # обмежуємо діапазон 1..5
        text = request.POST.get('text', '').strip()[:5000]

        if author and text and not spam_blocked and not cooldown_blocked:
            Review.objects.create(
                author=author,
                child_group=child_group,
                rating=rating,
                text=text,
                is_approved=False,
            )
            request.session['last_review_ts'] = now_ts
            submitted = True
        elif spam_blocked:
            # Удаємо для бота, що все добре, але нічого не зберегли
            submitted = True

    # Статистика — рахуємо на всіх схвалених відгуках, перед фільтрацією
    total = base_qs.count()
    avg = base_qs.aggregate(a=Avg('rating'))['a']
    stats = {
        'total': total,
        'avg':   round(avg, 1) if avg else 0,
        'one':   base_qs.filter(rating=1).count(),
        'two':   base_qs.filter(rating=2).count(),
        'three': base_qs.filter(rating=3).count(),
        'four':  base_qs.filter(rating=4).count(),
        'five':  base_qs.filter(rating=5).count(),
    }

    # Фільтрація за зірками
    star_filter = request.GET.get('stars', 'all')
    qs = base_qs
    if star_filter in {'1', '2', '3', '4', '5'}:
        qs = qs.filter(rating=int(star_filter))

    # Сортування
    sort = request.GET.get('sort', 'newest')
    if sort not in SORT_ORDERS:
        sort = 'newest'
    qs = qs.order_by(*SORT_ORDERS[sort])

    return render(request, 'reviews/reviews_page.html', {
        'reviews':        qs,
        'stats':          stats,
        'submitted':      submitted,
        'cooldown_blocked': cooldown_blocked,
        'cooldown_seconds': REVIEW_COOLDOWN_SECONDS,
        'filter_stars':   star_filter,
        'sort':           sort,
        'filtered_count': qs.count(),
    })
