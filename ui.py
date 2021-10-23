import click

from config import DB_URL
from db import Database


@click.group()
def ui():
    pass

@ui.group('db')
def ui_db():
    pass

"""
Usage:
    python ui.py db reset
"""
@ui_db.command('reset')
def ui_db_reset():
    database = Database(url=DB_URL)
    database.reset()

if __name__ == '__main__':
    ui()
