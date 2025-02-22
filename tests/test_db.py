import sqlite3
import pytest


@pytest.fixture
def cursor():
    cnxn = sqlite3.connect("../pokedex.db")
    cur = cnxn.cursor()

    return cur


def test_basic(cursor):
    query = "SELECT * FROM pokemon WHERE gen = 1 AND type1 = 'steel' OR type2 = 'steel'"

    res = cursor.execute(query)
    print(res.fetchone())
    

    assert 1 == 1