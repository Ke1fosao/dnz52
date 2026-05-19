from django.shortcuts import render, get_object_or_404
from .models import SpecialistPage


def specialist_page(request, page_type):
    """Сторінка спеціаліста"""
    page = get_object_or_404(SpecialistPage, page_type=page_type)
    specialists = page.specialists.prefetch_related('albums__album__photos').all()
    return render(request, 'specialists/specialist_page.html', {
        'page':        page,
        'specialists': specialists,
        'page_type':   page_type,
    })
