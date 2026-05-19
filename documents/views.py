from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Document, DocumentCategory


def documents_list(request):
    """Список документів"""
    documents = Document.objects.filter(is_published=True)
    categories = DocumentCategory.objects.all()

    context = {
        'documents': documents,
        'categories': categories,
    }
    return render(request, 'documents/documents_list.html', context)


def document_download(request, pk):
    """Завантаження документа"""
    document = get_object_or_404(Document, pk=pk)
    document.downloads += 1
    document.save()
    return FileResponse(document.file.open('rb'), as_attachment=True, filename=document.file.name)