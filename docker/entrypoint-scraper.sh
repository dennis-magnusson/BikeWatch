#!/bin/sh
cd /app

DB_PATH=$(echo "$SQLALCHEMY_DATABASE_URL" | sed 's/sqlite:\/\///')
mkdir -p "$(dirname "$DB_PATH")"

if [ ! -f "$DB_PATH" ]; then
    touch "$DB_PATH"
    echo "Created database file at $DB_PATH"
fi

alembic upgrade head
python src/main.py