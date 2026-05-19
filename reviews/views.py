from django.shortcuts import render
from django.db.models import Avg
from .models import Review


SORT_ORDERS = {
    'newest':  ('-created_at',),
    'oldest':  ('created_at',),
    'highest': ('-rating', '-created_at'),
    'lowest':  ('rating', '-created_at'),
}


def reviews_page(request):
    """Сторінка відгуків з фільтрацією за оцінкою та сортуванням."""
    base_qs = Review.objects.filter(is_approved=True)
    submitted = False

    if request.method == 'POST':
        author      = request.POST.get('author', '').strip()
        child_group = request.POST.get('child_group', '').strip()
        rating      = int(request.POST.get('rating', 5) or 5)
        text        = request.POST.get('text', '').strip()

        if author and text:
            Review.objects.create(
                author=author,
                child_group=child_group,
                rating=rating,
                text=text,
                is_approved=False,
            )
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
        'filter_stars':   star_filter,
        'sort':           sort,
        'filtered_count': qs.count(),
    })
