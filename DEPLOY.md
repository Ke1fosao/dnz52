# 🚀 Гайд із деплою — ЗДО №52

Покрокова інструкція як завантажити сайт у інтернет.

---

## 📦 Зміст
1. [Що вже зроблено](#що-вже-зроблено)
2. [Підготовка GitHub](#частина-1-github)
3. [Деплой на PythonAnywhere](#частина-2-pythonanywhere-рекомендовано)
4. [Альтернатива: Render](#частина-3-альтернатива--rendercom)
5. [Оновлення сайту після змін](#частина-4-як-оновлювати-сайт)
6. [Резервні копії](#частина-5-резервні-копії)
7. [Поширені проблеми](#часті-проблеми)

---

## Що вже зроблено

- ✅ Створено `requirements.txt` з усіма залежностями
- ✅ `settings.py` готовий до продакшену (читає змінні з `.env`)
- ✅ Налаштовано **WhiteNoise** для статики у продакшені
- ✅ `.env.example` — шаблон змінних середовища
- ✅ `.gitignore` — приховує секрети та локальні файли

---

## Частина 1. GitHub

### Що таке GitHub?
Це безкоштовний «хмарний диск для коду». Ви туди заливаєте свій проект — і хостинг забирає його одним кліком. Альтернативно можна без GitHub (через ZIP), але це менш зручно для оновлень.

### Крок 1.1 — Створіть обліковий запис
1. Відкрийте **[github.com](https://github.com)**
2. **Sign up** → email, пароль, username (наприклад `dnz52rivne`)
3. Підтвердіть email

### Крок 1.2 — Створіть репозиторій
1. Угорі справа: **«+»** → **«New repository»**
2. **Repository name:** `dnz52` (або як хочете)
3. **Description:** «Сайт ЗДО №52, м. Рівне»
4. **Public** (безкоштовно) або **Private** (теж безкоштовно — нікого крім вас не пускає)
5. ❌ **НЕ** ставте галочки «Add README», «Add .gitignore», «Add license» — у вас вже все є
6. **Create repository**

GitHub покаже екран з командами. Не виконуйте їх — ми будемо діяти інакше.

### Крок 1.3 — Встановіть Git
Якщо ще не встановлено: **[git-scm.com/download/win](https://git-scm.com/download/win)** → завантажте, встановіть «з настройками за замовчуванням».

Після встановлення перезапустіть PowerShell.

### Крок 1.4 — Завантажте проект на GitHub

Відкрийте **PowerShell** і виконайте по черзі:

```powershell
# Перейти у папку проекту
cd F:\Project\dnz52

# Видалити старий git якщо був (на всяк випадок)
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue

# Ініціалізувати новий git-репозиторій
git init

# Налаштувати ваше ім'я та email (один раз для всього компʼютера)
git config --global user.name "Дмитро"
git config --global user.email "ваш-email@gmail.com"

# Додати всі файли (крім тих, що в .gitignore)
git add .

# Створити перший коміт
git commit -m "Initial commit: site ZDO 52"

# Підключити до GitHub-репозиторію (замініть YOUR-USERNAME!)
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/dnz52.git

# Залити проект
git push -u origin main
```

GitHub попросить логін. **НЕ вводьте звичайний пароль!** Натомість:
1. На GitHub → **Settings** (профіль угорі справа) → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
2. **Note:** «git-cli», **Expiration:** «No expiration», **Scopes:** позначте `repo`
3. **Generate token** → скопіюйте довгий рядок (показується лише раз!)
4. Цей рядок — ваш «пароль» для git push

### ⚠️ ВАЖЛИВО: перевірте, що `.env` НЕ потрапив на GitHub
Відкрийте на GitHub ваш репозиторій. Файлу `.env` бути не повинно. Якщо є — терміново:
1. Згенеруйте новий SECRET_KEY (старий скомпрометований)
2. Видаліть `.env` з історії git

---

## Частина 2. PythonAnywhere (рекомендовано)

### Чому PythonAnywhere?
- ✅ Безкоштовно назавжди
- ✅ Не засинає (на відміну від Render)
- ✅ Без credit card
- ✅ Налаштовується через зрозумілий веб-інтерфейс

### Обмеження безкоштовного плану
- 1 веб-додаток · 512 MB диску · ~100 сек CPU/день
- Лише субдомен `username.pythonanywhere.com` (не власний домен)

### Крок 2.1 — Реєстрація
1. **[pythonanywhere.com](https://www.pythonanywhere.com)**
2. **Pricing & signup** → **Create a Beginner account**
3. Username (наприклад `dnz52rivne`) → це буде у вашій URL: `dnz52rivne.pythonanywhere.com`
4. Підтвердіть email

### Крок 2.2 — Завантажте код з GitHub
У PythonAnywhere: вгорі **Consoles** → **«Bash»** (відкриється чорна консоль).

```bash
# Завантаження коду з GitHub (замініть YOUR-USERNAME!)
git clone https://github.com/YOUR-USERNAME/dnz52.git

# Заходимо в папку проекту
cd dnz52

# Створюємо віртуальне середовище
mkvirtualenv --python=python3.11 dnz52-venv

# Встановлюємо залежності (займе 3-5 хвилин)
pip install -r requirements.txt
```

### Крок 2.3 — Створіть `.env` на сервері
У тій же Bash-консолі:
```bash
# Згенерувати свіжий SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Скопіюйте отриманий рядок.

Створіть `.env`:
```bash
nano .env
```
Вставте (Ctrl+Shift+V), замінивши `dnz52rivne` на ваш username:
```
SECRET_KEY=<сюди вставте згенерований ключ>
DEBUG=False
ALLOWED_HOSTS=dnz52rivne.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://dnz52rivne.pythonanywhere.com
```
Збережіть: **Ctrl+O → Enter → Ctrl+X**.

### Крок 2.4 — Міграції та статика
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
# (вкажіть свій логін/email/пароль адміна)
```

### Крок 2.5 — Налаштування Web app
1. Вгорі: **Web** → **Add a new web app**
2. **Next** → **Manual configuration** (НЕ Django!) → **Python 3.11** → **Next**
3. Тепер на сторінці налаштувань заповніть:

| Поле | Значення |
|------|----------|
| **Source code** | `/home/dnz52rivne/dnz52` |
| **Working directory** | `/home/dnz52rivne/dnz52` |
| **Virtualenv** (в розділі Virtualenv) | `/home/dnz52rivne/.virtualenvs/dnz52-venv` |

### Крок 2.6 — WSGI файл
Натисніть на посилання поряд з **WSGI configuration file**. Відкриється редактор. **Видаліть весь вміст** і вставте:

```python
import os
import sys
from dotenv import load_dotenv

# Шлях до проекту (ЗАМІНІТЬ dnz52rivne на свій username!)
path = '/home/dnz52rivne/dnz52'
if path not in sys.path:
    sys.path.insert(0, path)

# Завантажуємо змінні з .env
load_dotenv(os.path.join(path, '.env'))

# Запускаємо Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'dnz52_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
**Save** (зверху).

### Крок 2.7 — Static & Media файли
На сторінці Web app, прокрутіть до **Static files**. Натисніть **«Enter URL»** і додайте 2 записи:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/dnz52rivne/dnz52/staticfiles` |
| `/media/` | `/home/dnz52rivne/dnz52/media` |

### Крок 2.8 — Запуск
Угорі сторінки Web app — велика зелена кнопка **🔄 Reload dnz52rivne.pythonanywhere.com**.

🎉 Відкрийте **`https://dnz52rivne.pythonanywhere.com`** — сайт працює!

### Крок 2.9 — Перенесення даних (опціонально)
Якщо хочете перенести всі ваші новини, фото, спеціалістів з локального ПК:

**На локальному ПК (PowerShell):**
```powershell
cd F:\Project\dnz52
.venv\Scripts\python.exe manage.py dumpdata `
    --natural-foreign --natural-primary `
    --exclude=auth.permission --exclude=contenttypes `
    --indent 2 -o data.json
```

**Завантажте `data.json` і всю папку `media/` на PythonAnywhere:**
- Через інтерфейс **Files** → перейдіть у `/home/dnz52rivne/dnz52/` → **Upload a file**
- Або через `scp`, якщо вмієте

**На PythonAnywhere (Bash консоль):**
```bash
cd ~/dnz52
python manage.py loaddata data.json
```

Натисніть **🔄 Reload**. Готово!

---

## Частина 3. Альтернатива — Render.com

Якщо хочете сучасніший інтерфейс і не проти що сайт «спить» 15 хв:

1. **[render.com](https://render.com)** → Sign up через GitHub
2. **New +** → **Web Service** → виберіть свій репозиторій
3. **Name:** `dnz52`
4. **Region:** Frankfurt (найближче до України)
5. **Build Command:**
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
6. **Start Command:**
   ```
   gunicorn dnz52_site.wsgi
   ```
7. **Instance Type:** Free
8. **Environment Variables** → додайте:
   - `SECRET_KEY` = (згенеруйте новий)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `dnz52.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://dnz52.onrender.com`
9. **Create Web Service**

⚠️ **Важливо для Render**: SQLite на Free плані **скидається при кожному перезапуску**. Треба підключити PostgreSQL:
- **New +** → **PostgreSQL** → Free → Create
- Скопіюйте «Internal Database URL»
- У вашому Web Service → Environment → додайте `DATABASE_URL` = (скопійований URL)

---

## Частина 4. Як оновлювати сайт

Коли локально щось змінили і хочете щоб з'явилось на сайті:

### На локальному ПК (PowerShell)
```powershell
cd F:\Project\dnz52
git status              # перевіряємо що готується до коміту
git add -A              # додаємо всі зміни (.gitignore ігнорує секрети)
git commit -m "Опис того що змінили (наприклад: 'Додано меню на тиждень')"
git push
```

> ⚠️ Якщо `git add -A` додає файли яких не повинно бути (наприклад `.env`,
> `db.sqlite3`, `media/`) — спочатку перевірте, чи вони у `.gitignore`,
> і прибравши через `git reset <шлях>`.

### На PythonAnywhere (Bash)
```bash
cd ~/dnz52
git pull
workon dnz52-venv

# Завжди безпечно запускати — якщо нових міграцій немає, нічого не зробить:
python manage.py migrate

# Завжди безпечно — підхопить нові CSS/JS/SVG/іконки:
python manage.py collectstatic --noinput

# Якщо у requirements.txt додані нові пакети:
pip install -r requirements.txt
```

Потім **Web → 🔄 Reload**.

> 💡 Маленька шпаргалка: команди `migrate` і `collectstatic` краще
> запускати **завжди** після `git pull`. Якщо змін немає — Django нічого
> не робить. Якщо є — підхопить. Це безпечніше ніж намагатися згадати,
> чи ви змінювали моделі/статику.

### На Render
Достатньо `git push` — Render автоматично перезбере і перезапустить.

---

## Частина 5. Резервні копії

**Рекомендую раз на тиждень:**

### На PythonAnywhere
```bash
cd ~/dnz52
# Експорт БД у текстовий файл
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=auth.permission --exclude=contenttypes \
    --indent 2 -o backup-$(date +%Y%m%d).json

# Архівувати media
tar czf media-$(date +%Y%m%d).tar.gz media/
```

Потім через **Files** на PythonAnywhere завантажте ці файли до себе на ПК.

---

## Часті проблеми

### «DisallowedHost at /» або «Bad Request (400)»
→ Перевірте `ALLOWED_HOSTS` у `.env`. Має містити ваш домен.

### Сайт відкривається, але без CSS/SVG
→ Не виконано `collectstatic`. Запустіть:
```bash
python manage.py collectstatic --noinput
```

### «CSRF verification failed»
→ Перевірте `CSRF_TRUSTED_ORIGINS` у `.env`. Має бути повний URL з `https://`.

### Помилка «no such table»
→ Не виконані міграції:
```bash
python manage.py migrate
```

### Не можу залогінитись в адмінку
→ Створіть суперюзера:
```bash
python manage.py createsuperuser
```

### «ModuleNotFoundError: No module named 'dotenv'»
→ Не активоване віртуальне середовище. На PythonAnywhere:
```bash
workon dnz52-venv
pip install -r requirements.txt
```

### `.env` випадково потрапив у git
1. Згенеруйте новий SECRET_KEY (старий вже скомпрометований)
2. Видаліть файл з історії:
```bash
git rm --cached .env
git commit -m "Remove .env from git"
git push
```
3. Переконайтесь що `.env` є в `.gitignore` (вже є)

---

## 📞 Корисні посилання

- **PythonAnywhere help:** https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- **Render docs:** https://render.com/docs/deploy-django
- **GitHub docs:** https://docs.github.com/en/get-started

Успіхів з деплоєм! 🚀
