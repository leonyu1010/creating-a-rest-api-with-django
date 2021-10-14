#!/bin/sh


echo "Initializing postgres db go go go..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "postgres database has initialized successfully"
fi

exec "$@"
