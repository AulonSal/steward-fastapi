"""Config of DB"""

from steward_fastapi.config.base import INSTANCE_DIR
from steward_fastapi.config.config import POSTGRES_CREDENTIALS

TIMEZONE = 'Asia/Kolkata'
USE_TIMEZONE = True

DB_MODELS = [
    'steward_fastapi.core.models.database',
    'aerich.models',
]
SQLITE_DB_PATH = str(INSTANCE_DIR / 'db.sqlite3')
SQLITE_DB_URL = 'sqlite://' + SQLITE_DB_PATH


# Originally generated using the simplest scheme for tortoise.backends.base.config_generator.generate_config()
CONFIG = {
    'connections':
        {
            'default':
                {
                    'engine': 'tortoise.backends.sqlite',
                    'credentials':
                        {
                            'journal_mode': 'WAL',
                            'journal_size_limit': 16384,
                            'file_path': SQLITE_DB_PATH,
                        },
                },
            'postgres':
                {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': POSTGRES_CREDENTIALS.copy(),
                },
        },
    'apps':
        {
            'models':
                {
                    'models': DB_MODELS,
                    'default_connection': 'postgres',
                },
        },
    'use_tz': USE_TIMEZONE,
    'timezone': TIMEZONE,
}

