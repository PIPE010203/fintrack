# Diagrama de la Base de Datos — FinTrack

```mermaid
erDiagram
    auth_user ||--o{ transacciones_gasto : "tiene"
    auth_user ||--o{ transacciones_ingreso : "tiene"
    auth_user ||--o{ presupuesto_presupuesto : "tiene"

    transacciones_gasto {
        int id PK
        int usuario_id FK
        varchar descripcion
        decimal monto
        varchar categoria
        date fecha
        datetime creado
    }

    transacciones_ingreso {
        int id PK
        int usuario_id FK
        varchar descripcion
        decimal monto
        varchar categoria
        date fecha
        datetime creado
    }

    presupuesto_presupuesto {
        int id PK
        int usuario_id FK
        varchar categoria
        decimal limite
        int mes
        int anio
    }
```

## Notas

- `categoria` en los 3 modelos es un `CharField` con opciones definidas en `transacciones/choices.py`
- `presupuesto_presupuesto` tiene una constraint `UNIQUE(usuario, categoria, mes, anio)`
- No hay modelos en `usuarios`, `dashboard` ni `chatbot`
- Se usa el `User` built-in de Django (`auth_user`)
