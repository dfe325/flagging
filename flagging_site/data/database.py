"""
This file should handle all database connection stuff, namely: writing and
retrieving data.
"""

import os
import psycopg2
from flask import app, g

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)

def get_db():
    if 'db' not in g:
        g.db = conn

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

try:
    cur = conn.cursor()
    cur.execute('SELECT 1')
except psycopg2.OperationalError:
    pass

conn.close()