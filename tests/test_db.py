import sqlite3
import pytest


@pytest.fixture
def cursor():
    cnxn = sqlite3.connect("pokedex.db")
    cur = cnxn.cursor()

    return cur


def test_pokemon_table_exists(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon'"

    res = cursor.execute(query)
    tablename = res.fetchone()

    assert tablename is not None
    assert tablename[0] == 'pokemon'


def test_last_dex_entry(cursor):
    query = "SELECT num FROM pokemon ORDER BY num DESC"

    res = cursor.execute(query)
    last_dex_num = res.fetchone()

    assert last_dex_num[0] == 1025