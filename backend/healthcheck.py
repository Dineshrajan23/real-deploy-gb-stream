import os
import sys
import psycopg2

try:

    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host=os.environ.get("DB_HOST"),
        port="5432",
        connect_timeout=5  
    )

    sys.exit(0)

except psycopg2.OperationalError as e:
    sys.stderr.write(f"Healthcheck failed: {e}\n")
    sys.exit(1)