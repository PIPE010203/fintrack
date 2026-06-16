# FinTrack — agent guide

## Overview

Django (no DRF) personal finance manager for Colombian users.  
5 apps under `core.settings`, SQLite, templates-only frontend.

## Setup & run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

`pip install` is the only setup step — no `npm`/`node_modules`.

## Developer commands

| Action | Command |
|---|---|
| Run dev server | `python manage.py runserver` |
| Run all tests | `python manage.py test` |
| Run one app tests | `python manage.py test <app>` (e.g. `transacciones`) |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |

## Architecture

- **`core/`** — Django project root (settings, root URLconf, ASGI/WSGI)
- **`usuarios/`** — auth (register/login/logout). Django built-in `UserCreationForm` + `AuthenticationForm`, no custom model.
- **`transacciones/`** — `Gasto`/`Ingreso` CRUD + PDF (reportlab) / Excel (openpyxl) report export
- **`presupuesto/`** — `Presupuesto` monthly per-category budgets (unique: user + category + month + year)
- **`dashboard/`** — monthly aggregates (income/expense cards, Chart.js doughnut by category)
- **`chatbot/`** — OpenAI chat (`gpt-3.5-turbo`) with real financial context injected as system prompt

### URL structure

Root `/` redirects to `/dashboard/`. All endpoints wrapped with `@login_required` except `usuarios` auth views.

| Prefix | App |
|---|---|
| `/admin/` | Django admin |
| `/usuarios/` | registro, login, logout |
| `/transacciones/` | gastos/ingresos CRUD + reporte + exportar (pdf/excel) |
| `/presupuesto/` | presupuesto list, create, delete |
| `/dashboard/` | monthly summary |
| `/chatbot/` | chat interface |

## Notable details

- **Locale**: `es-co`, timezone `America/Bogota` (settings.py:73-74)
- **Auth**: Django `User` model, `LOGIN_URL = '/usuarios/login/'`, `LOGIN_REDIRECT_URL = '/dashboard/'`
- **No static assets locally** — Bootstrap 5, Bootstrap Icons, Chart.js all loaded from CDN
- **`.env` required keys**: `SECRET_KEY`, `DEBUG`, `OPENAI_API_KEY` (latter needed for chatbot, app still works without it — errors surfaced in chat)
- **Tests**: `tests.py` files exist in all apps but are empty stubs (just `from django.test import TestCase`). No test coverage to maintain.
- **No lint/typecheck config** — standard Django project, no ruff/black/mypy set up
