#!/bin/bash
echo "Creating Migrations..."
python ./src/manage.py makemigrations
python ./src/manage.py makemigrations spreadsheets
echo "===================================="

echo "Starting Migrations..."
python ./src/manage.py migrate
python ./src/manage.py migrate spreadsheets
echo "===================================="

echo "Checking if Super User Exists..."
user_exists=$(python ./src/manage.py shell -i python -c "from django.contrib.auth.models import User; print(User.objects.filter(username='admin').exists())")

if [ "$user_exists" = "False" ]; then
    echo "Creating Super User..."
    python ./src/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
else
    echo "Super User 'admin' already exists, skipping creation."
fi
echo "===================================="

echo "Starting Server..."
python ./src/manage.py runserver 0.0.0.0:8000