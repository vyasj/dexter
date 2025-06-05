import requests

import sqlite3
import json

from endpoints import POKEMON_ENDPOINT


def create():

    conn = sqlite3.connect("../dexter.db")

    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS
                pokemon(
                )""")
    
    conn.commit()
    cur.close()

    return


if __name__ == "__main__":
    # test to make sure api gives expected results
    # move this to unit test later?

    url =  POKEMON_ENDPOINT + "bulbasaur/"
    r = requests.get(url).json()

    print(r.keys())

    pass