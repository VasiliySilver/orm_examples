import os
from dotenv import load_dotenv

load_dotenv()

# Получение параметров подключения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "orm_examples")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Формирование URL подключений
SYNC_DATABASE_URL = os.getenv(
    "SYNC_DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

ASYNC_DATABASE_URL = os.getenv(
    "ASYNC_DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Для asyncpg (dict с параметрами)
ASYNCPG_CONFIG = {
    "host": DB_HOST,
    "port": int(DB_PORT),
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

# Настройки для отладки
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ECHO_SQL = os.getenv("ECHO_SQL", "True").lower() == "true"