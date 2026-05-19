from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, NewsCategory


def news_list(request):
    """Список всіх новин"""
    news = News.objects.filter(is_published=True)
    paginator = Paginator(news, 9)  # 9 новин на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = NewsCategory.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, slug):
    """Деталі новини"""
    news = get_object_or_404(News, slug=slug, is_published=True)
    news.views += 1
    news.save()
    related_news = News.objects.filter(is_published=True).exclude(pk=news.pk)[:5]
    categories = NewsCategory.objects.all()
    context = {
        'news': news,
        'related_news': related_news,
        'categories': categories,
    }
    return render(request, 'news/news_detail.html', context)


def news_by_category(request, slug):
    """Новини по категорії"""
    category = get_object_or_404(NewsCategory, slug=slug)
    news = News.objects.filter(category=category, is_published=True)
    paginator = Paginator(news, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': NewsCategory.objects.all(),
    }
    return render(request, 'news/news_by_category.html', context)
