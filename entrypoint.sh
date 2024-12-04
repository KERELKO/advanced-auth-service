#!/bin/sh

# Function to initialize the database tables
init_db_tables() {
    echo "Initializing database tables..."
    python3 -c "
from src.core.storage.orm.config import Database
from src.core.di import container
db = container.resolve(Database)
db.init()
"
    echo "Database tables initialized."
}

# Function to start the FastAPI application
start_fastapi_app() {
    echo "Starting FastAPI application..."
    uvicorn main:app_factory --reload --host 0.0.0.0 --port 8000 --factory
}

# Run the init_db_tables function
init_db_tables

sleep 5

# Run the start_fastapi_app function
start_fastapi_app
