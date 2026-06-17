# FinTrack — Personal Finance Manager

Personal finance tracking web application for Colombian users, built with Django.

## Features

- **Expense & Income tracking** — Register and categorize your daily transactions
- **Monthly budgets** — Set spending limits per category with visual progress bars
- **Dashboard** — Monthly summary with income/expense cards and Chart.js doughnut chart
- **Reports** — Export financial reports as PDF or Excel files
- **AI Assistant** — Chat with an OpenAI-powered assistant that has access to your financial data

## Requirements

- Python 3.10+
- Django 6.0+

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url> fintrack
cd fintrack

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your SECRET_KEY and OPENAI_API_KEY

# 4. Initialize database
python manage.py migrate

# 5. Create admin user (optional)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
```

Visit http://localhost:8000 and register your account.

## Environment Variables

| Key | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | Set to `True` for development |
| `OPENAI_API_KEY` | No* | OpenAI API key for chatbot |

*\* Chatbot feature won't work without it, rest of the app functions normally.*

## Project Structure

```
fintrack/
├── core/               # Django project settings & root URLconf
├── usuarios/           # User registration, login, logout
├── transacciones/      # Expenses & income CRUD + report export
├── presupuesto/        # Monthly budget management
├── dashboard/          # Monthly financial summary
├── chatbot/            # AI-powered financial assistant
├── templates/          # Django templates (Bootstrap 5)
└── static/             # Static files (empty — all from CDN)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0 (no DRF) |
| Frontend | Django templates, Bootstrap 5, Chart.js |
| Database | SQLite |
| PDF Export | ReportLab |
| Excel Export | Openpyxl |
| AI Chat | OpenAI GPT-3.5-turbo |
| CSS Icons | Bootstrap Icons |

## Developer Commands

| Action | Command |
|---|---|
| Run server | `python manage.py runserver` |
| Run all tests | `python manage.py test` |
| Run app tests | `python manage.py test <app_name>` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Django shell | `python manage.py shell` |

## URL Map

| Prefix | Description |
|---|---|
| `/` | Redirects to `/dashboard/` |
| `/admin/` | Django admin interface |
| `/usuarios/` | Register, login, logout |
| `/transacciones/` | CRUD for expenses & income |
| `/transacciones/reporte/` | Report generator |
| `/presupuesto/` | Budget management |
| `/dashboard/` | Monthly summary |
| `/chatbot/` | AI assistant chat |

## License

MIT
## Integrantes
-Andres Perez
-Jean Franco Muñoz
-Helen Florez
-Luis Lopez Fernandez
