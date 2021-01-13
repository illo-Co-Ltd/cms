#!/bin/bash

HOST="db"
PORT=3306

# Wait for the postgres docker to be running
while ! nc $HOST $PORT; do
  >&2 echo "Database is unavailable. Sleeping..."
  sleep 1
done
echo "Database container created and set."
# Apply database migrations
echo "Applying database migrations..."