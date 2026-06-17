# Django Best Practices — FinTrack

Coding conventions for this project based on Django official style and common best practices.

## Imports

- Standard library → Django → Third-party → Local, one group per line break
- Use explicit relative imports within apps: `from .models import Gasto`

```python
import os
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from openai import OpenAI

from .models import Gasto
```

## Views

- All views requiring auth: decorate with `@login_required`
- Use `get_object_or_404` with `usuario=request.user` to scope queries
- Use `ModelForm` for creation/editing, pass `instance=` for updates
- Return `redirect()` with named URL patterns after successful mutations

```python
@login_required
def edit_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk, usuario=request.user)
    form = GastoForm(request.POST or None, instance=gasto)
    if form.is_valid():
        form.save()
        return redirect('gastos')
    return render(request, 'transacciones/form_gasto.html', {'form': form})
```

## Models

- Use `Meta.ordering` for default sort order (descending by date)
- Use `choices` with tuples for category fields, display via `get_FOO_display()`
- ForeignKey to `User`: use `on_delete=models.CASCADE`
- Use `unique_together` for composite unique constraints

## Templates

- Extend `base.html` which provides Bootstrap 5 + sidebar layout
- Use `{% url 'name' %}` template tag for URL references
- Keep business logic in views, not templates
- Use Bootstrap classes: `card shadow`, `table table-hover`, `btn btn-{color}`

## URLs

- Each app has its own `urls.py`, included in `core/urls.py` with `include()`
- Use named URL patterns: `name='gastos'`
- Root `/` redirects to `/dashboard/`

## Tests

- All tests inherit from `django.test.TestCase`
- Test files live in each app's `tests.py`
- Use `django.test.Client` for view-level functional tests
- Use `setUpTestData` or `setUp` for shared fixtures
- Name test methods: `test_{verb}_{noun}` e.g. `test_create_gasto`

## Security

- Never hardcode secrets — use `.env` via `python-dotenv`
- `.env` is gitignored; provide `.env.example` with placeholder values
- Scope queries to `usuario=request.user` to prevent cross-user data access
- Use `@require_POST` on mutating AJAX endpoints
