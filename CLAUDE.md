# CLAUDE.md

## Про проєкт

Навчальний сайт на Django — список задач. Можна додати задачу, позначити виконаною, повернути назад і видалити.
Без JavaScript, без реєстрації, спільний список для всіх. База — SQLite (`db.sqlite3`). README.md написаний російською.

## Стек

- Python 3.10+ (у `.venv` — 3.12), Django (версія в `requirements.txt`)
- SQLite, Django Templates, CSS у `<style>` всередині шаблону

## Структура

- `manage.py` — точка входу.
- `config/` — налаштування (`settings.py`), кореневі URL (`urls.py`), `wsgi.py`.
- `tasks/` — єдиний застосунок:
  - `models.py` — модель `Task`: `title` (CharField, max 200), `done` (BooleanField).
  - `forms.py` — `TaskForm` (ModelForm, поле `title`).
  - `views.py` — `index` (GET показує список, POST додає задачу), `toggle` і `delete` (тільки POST, `@require_POST`).
  - `urls.py` — namespace `tasks`: `index`, `toggle` (`tasks/<pk>/toggle/`), `delete` (`tasks/<pk>/delete/`).
  - `templates/tasks/index.html` — єдиний шаблон.
  - `migrations/0001_initial.py` — початкова міграція.
  - `tests.py` — тести.

## Команди (Windows, PowerShell)

Активувати оточення не потрібно, використовуємо Python з `.venv` напряму:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver      # http://127.0.0.1:8000/
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

Після зміни моделей: `manage.py makemigrations`, потім `manage.py migrate`.

## Конвенції

- Після успішного POST завжди `redirect` (шаблон Post/Redirect/Get).
- Усі зміни даних — тільки через POST із `{% csrf_token %}` у формі.
- Для неіснуючих записів використовуємо `get_object_or_404`.
- Коментарі в коді та тексти інтерфейсу — російською, проєкт навчальний, тому код має лишатися простим і зрозумілим новачку.
- Налаштування мінімальні: у `INSTALLED_APPS` лише `tasks`, без admin, sessions, messages, staticfiles. Не додавай зайвого без потреби.

## Тести

У `tasks/tests.py` перевіряються: повний цикл створення/перемикання/видалення, валідація (порожній, пробіли, >200 символів), 404 для неіснуючих задач, 405 на GET, CSRF, екранування HTML. Нову функціональність покривай тестами в тому ж стилі (`TestCase`, `reverse("tasks:...")`).

## Обмеження

- `SECRET_KEY` і `DEBUG = True` прописані в коді — лише для локального запуску. Для публікації потрібні production-налаштування, секрет поза кодом і розмежування доступу.
- `db.sqlite3`, `.venv/`, `__pycache__/` у `.gitignore`. Git-репозиторій ще не ініціалізовано.
