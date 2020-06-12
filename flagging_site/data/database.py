"""
This file should handle all database connection stuff, namely: writing and
retrieving data.
"""

#source: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

import psql
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = psql.connect(
            current_app.config['crwa_flagging'],
            detect_types=psql.PARSE_DECLTYPES
        )
        g.db.row_factory = psql.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)