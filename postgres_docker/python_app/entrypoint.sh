#!/bin/sh

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Start application
exec fastapi run app.py --port $APP_PORT