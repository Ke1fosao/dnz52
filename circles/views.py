from django.shortcuts import render
from .models import Circle, CircleDocument


def circles_page(request):
    circles   = Circle.objects.filter(is_published=True)
    doc_links = CircleDocument.objects.select_related('document').all()
    return render(request, 'circles/circles_page.html', {
        'circles':   circles,
        'doc_links': doc_links,
    })
