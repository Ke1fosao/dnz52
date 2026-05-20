import re
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse, NoReverseMatch
from django.utils.html import strip_tags

from .models import (
    Page, Slider, Contact,
    ParentsAnnouncement, ParentsDocument, ParentsAdaptationPhoto, ParentsEnrollmentDoc,
    ParentsApplicationSample, StaffMember,
)
from news.models import News
from groups.models import Group
from circles.models import Circle
from specialists.models import Specialist, SpecialistPage
from gallery.models import GalleryAlbum
from documents.models import Document


def home(request):
    """Головна сторінка"""
    sliders = Slider.objects.filter(is_active=True)
    latest_news = News.objects.filter(is_published=True)[:6]

    context = {
        'sliders': sliders,
        'latest_news': latest_news,
    }
    return render(request, 'main/home.html', context)


def page_detail(request, slug):
    """Сторінка статичного контенту. Деякі slug'и мають кастомні шаблони."""
    page = get_object_or_404(Page, slug=slug, is_published=True)

    if slug == 'parents':
        return _render_parents_page(request, page)

    if slug == 'staff':
        return _render_staff_page(request, page)

    return render(request, 'main/page_detail.html', {'page': page})


def _render_staff_page(request, page):
    """Окремий рендер для сторінки «Керівництво» з карткою-портретом директора + сітка."""
    staff_qs = StaffMember.objects.filter(is_active=True)
    featured = staff_qs.filter(is_featured=True)
    others = staff_qs.filter(is_featured=False)
    return render(request, 'main/staff_page.html', {
        'page': page,
        'featured_members': featured,
        'other_members': others,
    })


def _render_parents_page(request, page):
    """Окремий рендер для батьківської сторінки з усіма секціями."""
    announcements = ParentsAnnouncement.objects.filter(is_active=True)
    documents = ParentsDocument.objects.filter(is_active=True)
    photos = ParentsAdaptationPhoto.objects.filter(is_active=True)
    enrollment_docs = ParentsEnrollmentDoc.objects.filter(is_active=True)
    application_samples = ParentsApplicationSample.objects.filter(is_active=True)
    adaptation_page = Page.objects.filter(slug='adaptation-advice', is_published=True).first()

    return render(request, 'main/parents_page.html', {
        'page': page,
        'announcements': announcements,
        'documents': documents,
        'photos': photos,
        'enrollment_docs': enrollment_docs,
        'application_samples': application_samples,
        'adaptation_page': adaptation_page,
    })


def contacts(request):
    """Сторінка контактів"""
    try:
        contact = Contact.objects.first()
    except Contact.DoesNotExist:
        contact = None
    return render(request, 'main/contacts.html', {'contact': contact})


# ============================================================================
# Кастомні сторінки помилок
# ============================================================================

def error_404(request, exception):
    """Сторінка 404 — не знайдено."""
    return render(request, '404.html', status=404)


def error_500(request):
    """Сторінка 500 — внутрішня помилка сервера."""
    return render(request, '500.html', status=500)


# ============================================================================
# Розумний пошук по сайту
# ============================================================================

def _safe_url(name, **kwargs):
    try:
        return reverse(name, kwargs=kwargs)
    except NoReverseMatch:
        return ''


def _clean(text, length=240):
    """Видаляє HTML-теги і скорочує текст."""
    if not text:
        return ''
    txt = strip_tags(str(text))
    txt = re.sub(r'\s+', ' ', txt).strip()
    if len(txt) > length:
        txt = txt[:length].rsplit(' ', 1)[0] + '…'
    return txt


def _snippet_around(text, terms, length=240):
    """Повертає короткий контекст довкола першого збігу пошукового слова."""
    if not text:
        return ''
    plain = strip_tags(str(text))
    plain = re.sub(r'\s+', ' ', plain).strip()
    lower = plain.lower()
    idx = -1
    for t in terms:
        i = lower.find(t.lower())
        if i != -1 and (idx == -1 or i < idx):
            idx = i
    if idx == -1:
        return plain[:length] + ('…' if len(plain) > length else '')
    start = max(0, idx - 60)
    end = min(len(plain), idx + length - 60)
    out = plain[start:end]
    if start > 0:
        out = '…' + out
    if end < len(plain):
        out = out + '…'
    return out


def _score(text, terms, weight=1):
    """Підрахунок вагового score для текстового поля."""
    if not text:
        return 0
    lower = strip_tags(str(text)).lower()
    return sum(lower.count(t.lower()) * weight for t in terms)


def search(request):
    """Розумний пошук по контенту сайту."""
    query = (request.GET.get('q') or '').strip()
    kind = (request.GET.get('kind') or '').strip()  # фільтр за типом

    results = []
    counts = {}

    if query and len(query) >= 2:
        # Розіб'ємо запит на слова (>=2 літери)
        raw_terms = [w for w in re.split(r'\s+', query) if len(w) >= 2]
        terms = raw_terms if raw_terms else [query]

        # ---------- News ----------
        news_q = Q()
        for t in terms:
            news_q |= Q(title__icontains=t) | Q(content__icontains=t)
        for n in News.objects.filter(news_q, is_published=True).distinct()[:60]:
            sc = _score(n.title, terms, 5) + _score(n.content, terms, 1)
            if sc <= 0:
                continue
            results.append({
                'type': 'Новина',
                'kind': 'news',
                'icon': 'bi-newspaper',
                'accent': 'primary',
                'title': n.title,
                'url': _safe_url('news:news_detail', slug=n.slug),
                'snippet': _snippet_around(n.content, terms),
                'date': n.created_at,
                'score': sc,
            })

        # ---------- Pages ----------
        page_q = Q()
        for t in terms:
            page_q |= Q(title__icontains=t) | Q(content__icontains=t)
        for p in Page.objects.filter(page_q, is_published=True).distinct()[:60]:
            sc = _score(p.title, terms, 5) + _score(p.content, terms, 1)
            if sc <= 0:
                continue
            results.append({
                'type': 'Сторінка',
                'kind': 'page',
                'icon': 'bi-file-earmark-text',
                'accent': 'info',
                'title': p.title,
                'url': _safe_url('main:page_detail', slug=p.slug),
                'snippet': _snippet_around(p.content, terms),
                'date': p.updated_at,
                'score': sc,
            })

        # ---------- Specialists ----------
        sp_q = Q()
        for t in terms:
            sp_q |= (Q(full_name__icontains=t) | Q(position__icontains=t)
                     | Q(bio__icontains=t) | Q(motto__icontains=t))
        for s in Specialist.objects.filter(sp_q).select_related('page').distinct()[:60]:
            sc = (_score(s.full_name, terms, 8) + _score(s.position, terms, 4)
                  + _score(s.bio, terms, 1) + _score(s.motto, terms, 2))
            if sc <= 0:
                continue
            results.append({
                'type': 'Спеціаліст',
                'kind': 'specialist',
                'icon': 'bi-person-badge',
                'accent': 'success',
                'title': f'{s.full_name} · {s.position}',
                'url': _safe_url('specialists:specialist_page', page_type=s.page.page_type),
                'snippet': _snippet_around(s.bio or s.motto, terms),
                'date': None,
                'score': sc,
            })

        # ---------- Staff (керівництво) ----------
        st_q = Q()
        for t in terms:
            st_q |= (Q(full_name__icontains=t) | Q(position__icontains=t)
                     | Q(awards__icontains=t) | Q(education__icontains=t))
        for st in StaffMember.objects.filter(st_q, is_active=True).distinct()[:60]:
            sc = (_score(st.full_name, terms, 8) + _score(st.position, terms, 4)
                  + _score(st.awards, terms, 2) + _score(st.education, terms, 1))
            if sc <= 0:
                continue
            results.append({
                'type': 'Керівництво',
                'kind': 'staff',
                'icon': 'bi-mortarboard',
                'accent': 'warning',
                'title': f'{st.full_name} · {st.position}',
                'url': _safe_url('main:page_detail', slug='staff'),
                'snippet': _clean(st.awards or st.education),
                'date': None,
                'score': sc,
            })

        # ---------- Groups ----------
        gr_q = Q()
        for t in terms:
            gr_q |= Q(name__icontains=t) | Q(description__icontains=t) | Q(motto__icontains=t)
        for g in Group.objects.filter(gr_q, is_published=True).distinct()[:30]:
            sc = (_score(g.name, terms, 6) + _score(g.description, terms, 1)
                  + _score(g.motto, terms, 3))
            if sc <= 0:
                continue
            results.append({
                'type': 'Група',
                'kind': 'group',
                'icon': 'bi-grid-3x3-gap',
                'accent': 'purple',
                'title': g.name,
                'url': _safe_url('groups:group_detail', slug=g.slug),
                'snippet': _clean(g.description),
                'date': None,
                'score': sc,
            })

        # ---------- Circles ----------
        cr_q = Q()
        for t in terms:
            cr_q |= (Q(name__icontains=t) | Q(description__icontains=t)
                     | Q(goal__icontains=t) | Q(leader__icontains=t))
        for c in Circle.objects.filter(cr_q, is_published=True).distinct()[:30]:
            sc = (_score(c.name, terms, 6) + _score(c.description, terms, 1)
                  + _score(c.goal, terms, 2) + _score(c.leader, terms, 3))
            if sc <= 0:
                continue
            results.append({
                'type': 'Гурток',
                'kind': 'circle',
                'icon': 'bi-stars',
                'accent': 'pink',
                'title': f'{c.name} · {c.leader}',
                'url': _safe_url('circles:circles_page'),
                'snippet': _clean(c.description or c.goal),
                'date': None,
                'score': sc,
            })

        # ---------- Documents ----------
        d_q = Q()
        for t in terms:
            d_q |= Q(title__icontains=t) | Q(description__icontains=t)
        for d in Document.objects.filter(d_q, is_published=True).distinct()[:30]:
            sc = _score(d.title, terms, 5) + _score(d.description, terms, 1)
            if sc <= 0:
                continue
            results.append({
                'type': 'Документ',
                'kind': 'document',
                'icon': 'bi-file-earmark-pdf',
                'accent': 'danger',
                'title': d.title,
                'url': _safe_url('documents:documents_list') + f'#doc-{d.pk}',
                'snippet': _clean(d.description),
                'date': d.created_at,
                'score': sc,
            })

        # ---------- Gallery albums ----------
        a_q = Q()
        for t in terms:
            a_q |= Q(title__icontains=t) | Q(description__icontains=t)
        for a in GalleryAlbum.objects.filter(a_q, is_published=True).distinct()[:30]:
            sc = _score(a.title, terms, 5) + _score(a.description, terms, 1)
            if sc <= 0:
                continue
            results.append({
                'type': 'Фотоальбом',
                'kind': 'album',
                'icon': 'bi-images',
                'accent': 'info',
                'title': a.title,
                'url': _safe_url('gallery:album_detail', slug=a.slug),
                'snippet': _clean(a.description),
                'date': a.created_at,
                'score': sc,
            })

        # ---------- Sort by relevance ----------
        results.sort(key=lambda r: (-r['score'], r['title'].lower()))

        # Counts per kind (для фільтра-чіпів)
        counts = {}
        for r in results:
            counts[r['kind']] = counts.get(r['kind'], 0) + 1

        # Фільтр за типом
        if kind:
            results = [r for r in results if r['kind'] == kind]

    # Пагінація
    paginator = Paginator(results, 12)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num) if results else None

    return render(request, 'main/search.html', {
        'query':   query,
        'results': results,
        'page_obj': page_obj,
        'total':   len(results),
        'counts':  counts,
        'kind':    kind,
    })
