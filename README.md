# ORM Examples: SQLAlchemy & asyncpg

Проект для экспериментов с различными подходами работы с БД в Python.

## Структура

- `sqlalchemy_examples/sync/` - синхронные примеры SQLAlchemy (ORM + raw SQL)
- `sqlalchemy_examples/async_orm/` - асинхронные примеры SQLAlchemy (ORM + raw SQL)
- `asyncpg_examples/` - примеры работы с asyncpg (только raw SQL)

```txt
orm_examples/
├── requirements.txt
├── README.md
├── .gitignore
├── sqlalchemy_examples/
│   ├── __init__.py
│   ├── sync/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── orm_queries.py
│   │   └── raw_queries.py
│   └── async_orm/
│       ├── __init__.py
│       ├── models.py
│       ├── orm_queries.py
│       └── raw_queries.py
├── asyncpg_examples/
│   ├── __init__.py
│   ├── basic_queries.py
│   └── advanced_queries.py
├── database/
│   ├── migrations/
│   └── seeds/
└── config.py
```

## Установка

```bash
# Установка uv (если еще не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установка зависимостей
uv sync
```

## Настройка

Скопируйте `.env.example` в `.env` и настройте подключение к БД:

```bash
cp .env.example .env
```

## Запуск примеров

```bash
# Синхронные примеры SQLAlchemy
uv run python -m sqlalchemy_examples.sync.orm_queries
uv run python -m sqlalchemy_examples.sync.raw_queries

# Асинхронные примеры SQLAlchemy
uv run python -m sqlalchemy_examples.async_orm.orm_queries
uv run python -m sqlalchemy_examples.async_orm.raw_queries

# Примеры asyncpg
uv run python -m asyncpg_examples.basic_queries
uv run python -m asyncpg_examples.advanced_queries
```