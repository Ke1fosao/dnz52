"""
Django settings for dnz52_site project.

ВАЖЛИВО: ніколи не комітьте файл .env у git!
Усі секрети (SECRET_KEY, паролі БД) задаються через .env
"""

import os
from pathlib import Path

from whitenoise.storage import CompressedManifestStaticFilesStorage


class ResilientStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Те саме, що й WhiteNoise CompressedManifestStaticFilesStorage,
    але не падає з 500-ю помилкою якщо у маніфесті немає якогось файлу.
    Натомість віддає звичайний (не хешований) URL.
    Це робить деплой стійким до того, що хтось забув запустити collectstatic.
    """
    manifest_strict = False


# Завантаження змінних з .env (якщо файл існує)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # У продакшені на деяких хостингах змінні задаються інакше

# ----------------------------------------------------------------------------
# Базові шляхи
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------------
# Безпека
# ----------------------------------------------------------------------------
# SECRET_KEY читається зі змінної середовища
# Якщо не задано — використовуємо devовий ключ (тільки для локальної розробки!)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-dev-key-CHANGE-ME-in-production-!!!'
)

# DEBUG — за замовчуванням False для безпеки. На локальному ПК у .env: DEBUG=True
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# Дозволені хости — додайте сюди адресу вашого сайту
# У .env: ALLOWED_HOSTS=dnz52.pythonanywhere.com,dnz52.com.ua
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',') if h.strip()
]

# CSRF — для HTTPS-сайтів обовʼязково
# У .env: CSRF_TRUSTED_ORIGINS=https://dnz52.pythonanywhere.com
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]


# ----------------------------------------------------------------------------
# Застосунки
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Sitemap для SEO
    'django.contrib.sitemaps',

    # Сторонні
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_bootstrap5',

    # Наші
    'main',
    'news',
    'gallery',
    'documents',
    'groups',
    'specialists',
    'circles',
    'reviews',
]


# ----------------------------------------------------------------------------
# Middleware
# ----------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — роздає статичні файли у продакшені (CSS/JS/SVG)
    # Має йти ОДРАЗУ після SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dnz52_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Папка templates/ на рівні проекту — для 404.html, 500.html, robots.txt
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dnz52_site.wsgi.application'


# ----------------------------------------------------------------------------
# База даних
# ----------------------------------------------------------------------------
# За замовчуванням — SQLite (підходить для маленького садочкового сайту).
# Якщо хостинг дає DATABASE_URL (Render, Railway тощо) — використовуємо її.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Підтримка DATABASE_URL для хостингів типу Render/Railway/Heroku
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    except ImportError:
        pass


# ----------------------------------------------------------------------------
# Паролі
# ----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ----------------------------------------------------------------------------
# Локалізація
# ----------------------------------------------------------------------------
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_TZ = True


# ----------------------------------------------------------------------------
# Статичні файли (CSS, JS, SVG)
# ----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise — стиснення + кешування.
# Використовуємо ResilientStaticFilesStorage (визначений вище), щоб сайт
# не падав з 500-ю, якщо у маніфесті немає файлу — поверне URL без хешу.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'dnz52_site.settings.ResilientStaticFilesStorage',
    },
}


# ----------------------------------------------------------------------------
# Медіа файли (фото, документи що завантажують користувачі)
# ----------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ----------------------------------------------------------------------------
# CKEditor
# ----------------------------------------------------------------------------
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}


# ----------------------------------------------------------------------------
# Crispy Forms
# ----------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# ----------------------------------------------------------------------------
# Default primary key
# ----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ----------------------------------------------------------------------------
# Безпека у продакшені (вмикається коли DEBUG=False)
# ----------------------------------------------------------------------------
if not DEBUG:
    # HTTPS перенаправлення (тільки якщо у вас точно є HTTPS)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    # HSTS — браузер запам'ятає, що до сайту тільки HTTPS (захист від downgrade)
    # 31536000 = 1 рік. Це безпечно для проду; на dev/staging — не вмикайте.
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Не відправляти Referer на сторонні сайти (приватність відвідувачів)
    SECURE_REFERRER_POLICY = 'same-origin'
