from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Page
from news.models import News
from groups.models import Group


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['main:home', 'main:contacts', 'news:news_list',
                'gallery:gallery_list', 'documents:documents_list',
                'groups:groups_list', 'reviews:reviews_page']

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/page/{obj.slug}/'


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/news/{obj.slug}/'


class GroupSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Group.objects.filter(is_published=True)

    def location(self, obj):
        return f'/groups/{obj.slug}/'
