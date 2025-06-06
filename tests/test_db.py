import sqlite3
import pytest


@pytest.fixture
def cursor():
    cnxn = sqlite3.connect("pokedex.db")
    cur = cnxn.cursor()

    return cur