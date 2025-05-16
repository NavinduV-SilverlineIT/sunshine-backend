#!/bin/bash

# Database credentials
DB_NAME="sunshine"
DB_USER="postgres"
DB_PASSWORD="postgres"

echo "Resetting database..."

# Run the SQL script
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -f reset_db.sql

# Remove old migrations
echo "Removing old migrations..."
rm -f vehicle_parts/migrations/0*.py

# Remove migration records from database
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -c "DELETE FROM django_migrations WHERE app = 'vehicle_parts';"

# Create fresh migrations
echo "Creating fresh migrations..."
python manage.py makemigrations vehicle_parts

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

echo "Database reset complete!" 