# Сайт ЗДО №52 м. Рівне

Веб-сайт закладу дошкільної освіти №52, розроблений на Django у рамках дипломної роботи.

---

## 📋 Опис системи

Інформаційно-довідковий сайт дитячого садка з можливістю керування контентом через адмінпанель Django. Призначений для батьків, педагогів та адміністрації закладу.

### Основні розділи

- **Головна** — слайдер, останні новини, переваги закладу
- **Новини** — публікації з категоріями, пагінацією та лічильником переглядів
- **Про заклад / Педагогам / Батькам** — статичні сторінки з WYSIWYG-редактором (CKEditor)
- **Групи** — інформація про вікові групи з вихователями та помічниками
- **Спеціалісти** — методист, психолог, музкерівник, медсестра, фізкультурний керівник
- **Гурткова робота** — описи гуртків з керівниками та розкладом
- **Фотогалерея** — альбоми з фотографіями
- **Документи** — нормативні документи з категоризацією та лічильником завантажень
- **Відгуки** — з модерацією, рейтингом, статистикою та захистом від спаму (honeypot)
- **Контакти** — адреса, телефони, карта Google Maps, соцмережі
- **Пошук** — глобальний пошук по новинах, сторінках та документах
- **Sitemap.xml + robots.txt** — для SEO

---

## 🛠 Технологічний стек

- **Python 3.12** + **Django 5.x**
- **SQLite** (для розробки; легко мігрує на PostgreSQL для продакшну)
- **CKEditor** — WYSIWYG-редактор
- **Bootstrap 5** + **Bootstrap Icons**
- **django-crispy-forms** + **crispy-bootstrap5**
- **Pillow** — обробка зображень
- **python-dotenv** — змінні оточення

---

## 🚀 Встановлення (Windows)

### 1. Розпакувати проєкт і відкрити термінал у папці `dnz52/`

### 2. Створити віртуальне середовище

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Встановити залежності

```powershell
pip install -r requirements.txt
```

### 4. Створити файл `.env` з конфігурацією

```powershell
copy .env.example .env
```

Згенерувати секретний ключ:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Відкрити `.env` у редакторі і вставити отриманий ключ у `DJANGO_SECRET_KEY=...`.

### 5. Застосувати міграції БД

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Створити суперкористувача (для адмінки)

```powershell
python manage.py createsuperuser
```

### 7. Запустити сервер

```powershell
python manage.py runserver
```

Сайт буде доступний на http://127.0.0.1:8000/
Адмінка — http://127.0.0.1:8000/admin/

---

## 📂 Структура проєкту

```
dnz52/
├── dnz52_site/          # Налаштування Django (settings, urls, wsgi)
├── main/                # Головна, статичні сторінки, контакти, пошук, sitemap
├── news/                # Новини з категоріями
├── gallery/             # Фотогалерея (альбоми + фото)
├── documents/           # Документи з категоріями
├── groups/              # Групи дітей та персонал
├── specialists/         # Сторінки спеціалістів
├── circles/             # Гуртки
├── reviews/             # Відгуки з модерацією
├── static/              # CSS, JS, зображення
│   ├── css/style.css
│   └── js/main.js
├── templates/           # Глобальні шаблони (404, 500, robots.txt)
├── media/               # Завантажені користувачем файли (створюється автоматично)
├── manage.py
├── requirements.txt
├── .env.example         # Приклад файлу конфігурації
├── .gitignore
└── README.md
```

---

## 🔧 Що було виправлено / додано (порівняно з попередньою версією)

### Виправлені баги

- Race condition у лічильнику переглядів новин — тепер через `F()`-expression
- Race condition у лічильнику завантажень документів — тепер через `F()`-expression
- Некоректний `try/except` у `contacts()` — `first()` не кидає виключення
- Ім'я файлу при завантаженні документа — використовується `os.path.basename`
- Слайдер на головній ламався без слайдів — додано `{% if sliders %}`
- Статистика відгуків — переписана на агрегації (`Avg`, `Count`) одним запитом
- Виправлено `TIME_ZONE` з `Europe/Kiev` на `Europe/Kyiv` (правильна назва)

### Безпека

- `SECRET_KEY` винесено у `.env` (з fallback для розробки)
- `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` керуються через `.env`
- Заголовки безпеки (HSTS, X-Frame-Options тощо) вмикаються автоматично при `DEBUG=False`
- Захист від спаму у формі відгуків через honeypot-поле
- Валідація форм (мінімальна/максимальна довжина)
- `.gitignore` правильно ігнорує `.env`, `db.sqlite3`, `media/`, `__pycache__/`

### Нові функції

- **Глобальний пошук** по сайту (новини, сторінки, документи) — `/search/?q=...`
- **Sitemap.xml** для пошуковиків
- **Robots.txt** з директивами
- **Кастомні сторінки 404 і 500**
- **Соцмережі** додано як поля у модель `Contact` (Facebook, Instagram, YouTube)
- **Кнопка "Нагору"** на всіх сторінках
- **Open Graph мета-теги** для соцмереж
- **Skip-to-content** посилання для доступності
- **Lazy-loading** зображень

### Якість коду

- Заповнено `requirements.txt`
- Додано `select_related` у views для зменшення кількості SQL-запитів
- Додано `get_absolute_url()` у модель `Page`
- Документація проєкту (цей README)

---

## 🎯 Що ще можна додати (рекомендації для розширення)

### Календар подій (новий додаток `events`)

Для дитсадка дуже актуально — ранки, дні відкритих дверей, батьківські збори. Модель:

```python
# events/models.py
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', blank=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL,
                              null=True, blank=True)
    is_published = models.BooleanField(default=True)
```

### Меню харчування (новий додаток `menu`)

Багато реальних сайтів ЗДО мають денне меню. Модель:

```python
# menu/models.py
class DailyMenu(models.Model):
    date = models.DateField(unique=True)
    breakfast = models.TextField()
    lunch = models.TextField()
    snack = models.TextField()
    is_published = models.BooleanField(default=True)
```

### FAQ (новий додаток `faq`)

Часті запитання — простий додаток для типових питань батьків.

### Інші ідеї

- **Онлайн-заявка на зарахування** — форма + email-сповіщення завідувачці
- **RSS-стрічка новин** — через `django.contrib.syndication` (20 рядків)
- **Кешування** — `cache_page` на головну, новини, документи
- **Тести** — додати тести у порожні `tests.py` (хоч 5-10 штук на основні views)
- **Перехід на CKEditor 5** — поточний CKEditor 4 у статусі EOL
- **Перехід на PostgreSQL для продакшну** — змінити `DATABASES` у `settings.py`
- **Docker + docker-compose** — для простого деплою
- **Деплой** — Render, Railway, Fly.io (безкоштовно для невеликих проєктів)

---

## 🔐 Адмінпанель

Після `python manage.py createsuperuser` зайди в http://127.0.0.1:8000/admin/

Через адмінку можна керувати:
- Сторінками, слайдером, контактами
- Новинами та категоріями
- Альбомами і фото
- Документами і категоріями
- Групами, вихователями, помічниками
- Спеціалістами і їхніми альбомами
- Гуртками та документами гуртків
- Модерацією відгуків

---

## 📄 Ліцензія

Проєкт розроблено як дипломну роботу. Усі права належать автору.

---

## ✉️ Контакти

Питання та пропозиції — через GitHub Issues або електронну пошту.
