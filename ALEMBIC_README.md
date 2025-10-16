# Alembic: Guía rápida de uso

## Instalación

```sh
pip install alembic
```

## Configuración inicial
- Edita `alembic.ini` y pon tu cadena de conexión en `sqlalchemy.url`.
- Revisa que `alembic/env.py` importe correctamente tus modelos (ya está preparado para SQLAlchemy y `db/models.py`).

## Comandos básicos

### 1. Inicializar el entorno (ya hecho)
Si no tienes la carpeta, ejecuta:
```sh
alembic init alembic
```

### 2. Crear una migración automática
```sh
alembic revision --autogenerate -m "Describe el cambio"
```

### 3. Aplicar migraciones
```sh
alembic upgrade head
```

### 4. Ver historial de migraciones
```sh
alembic history
```

### 5. Revertir a una versión anterior
```sh
alembic downgrade <revision>
```

## Consejos
- Haz commit de los archivos en `alembic/versions/`.
- Revisa los scripts generados antes de aplicar en producción.
- Puedes editar los scripts para añadir lógica personalizada (valores por defecto, migración de datos, etc).

---

Para más información: https://alembic.sqlalchemy.org/en/latest/
