#!/bin/sh

# Function to initialize the database tables
init_db_tables() {
    echo "Initializing database tables..."
    python3 -c "
from src.core.storages.db import Database
from src.core.di import container
db = container.resolve(Database)
db.init()
"
    echo "Database tables initialized."
}

# Run the init_db_tables function
init_db_tables

uvicorn main:app --reload --port 8000 --host 0.0.0.0
