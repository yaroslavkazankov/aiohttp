import os

engine = os.environ.get("SQL_ENGINE", "postgresql+asyncpg")
user = os.environ.get("SQL_USER", "netology_flask")
password = os.environ.get("SQL_PASSWORD", "flask")
port = os.environ.get("SQL_PORT", 5432)
db_name = os.environ.get("SQL_DATABASE", "netology_flask")
host = os.environ.get("SQL_HOST", "postgres")

URI = f'{engine}://{user}:{password}@{host}:{port}/{db_name}'
