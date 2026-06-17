# FinTrack — Development Skills

Workflows and patterns used when developing this project.

## Adding a New Feature

1. Create or update the model in the relevant app
2. Run `python manage.py makemigrations && python manage.py migrate`
3. Register model in `admin.py` if admin panel access is needed
4. Create `ModelForm` in `forms.py` if user-facing CRUD is needed
5. Add views in `views.py` with `@login_required`
6. Wire URLs in the app's `urls.py` + `core/urls.py`
7. Create templates extending `base.html`
8. Write tests in the app's `tests.py`
9. Run `python manage.py test <app_name>` to verify

## Exporting Reports

The app supports PDF and Excel export via `transacciones/views.py`:
- PDF uses ReportLab `SimpleDocTemplate` with styled `Table` elements
- Excel uses Openpyxl with styled sheets (Gastos, Ingresos, Resumen)
- Both accept `mes`, `anio`, and `todo` GET parameters
- The `todo=1` flag exports the entire history

## AI Chatbot

The chatbot at `/chatbot/`:
- Uses OpenAI `gpt-3.5-turbo` with real financial context injected as system prompt
- Sends current month's income/expense/balance + per-category breakdown
- Works without an API key — errors are surfaced in the UI
- CSRF token passed via `X-CSRFToken` header in JavaScript fetch calls

## Testing

- Run all tests: `python manage.py test`
- Run single app: `python manage.py test transacciones`
- No external services required for test execution
- Tests use SQLite in-memory database automatically
- Existing tests are stubs; real tests are in `tests.py` per app

## Deployment Notes

- `ALLOWED_HOSTS = ['*']` in settings — restrict for production
- `DEBUG` is hardcoded `True` — use `.env` in production
- No static files collected — all assets served from CDN
- SQLite is not suitable for production at scale
