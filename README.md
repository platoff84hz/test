# Сайт кафедры ИС на Django

Монолитное MVC-приложение с серверной генерацией HTML: Django, SQLite, Bootstrap 5.

## Запуск

```powershell
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_demo
.\.venv\Scripts\python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Демонстрационные учетные записи

- Администратор: `admin` / `admin123`
- Преподаватель: `teacher` / `teacher123`

Администратор управляет преподавателями и направлениями. Преподаватель редактирует только собственную карточку.
