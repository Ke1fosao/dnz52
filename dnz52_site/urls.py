from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from main.sitemaps import (
    StaticViewSitemap, PageSitemap, NewsSitemap, GroupSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'pages':  PageSitemap,
    'news':   NewsSitemap,
    'groups': GroupSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),

    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('gallery/', include('gallery.urls')),
    path('documents/', include('documents.urls')),
    path('groups/', include('groups.urls')),
    path('specialists/', include('specialists.urls')),
    path('circles/', include('circles.urls')),
    path('reviews/', include('reviews.urls')),
    path('menu/', include('menu.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Кастомні сторінки помилок (підхоплюються Django автоматично коли DEBUG=False)
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
