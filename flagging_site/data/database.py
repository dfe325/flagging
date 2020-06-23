"""
This file should handle all database connection stuff, namely: writing and
retrieving data.
"""

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(database=DATABASE_URL, user='postgres', host='localhost', password='postgrespw', port=5432)

#conn.close()

print(conn.closed)

try:
    cur = conn.cursor()
    cur.execute('SELECT 1')
except psycopg2.OperationalError:
    pass

print(conn.closed) # 2