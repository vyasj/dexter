import requests
import sqlite3
import os
import time
import logging


def download(batch_size):
    base_url = "https://img.pokemondb.net/sprites"
    files = os.listdir("images/")
    try:
        last_dir = files[-1]
        num_left_off = int(last_dir.split("_")[0])
    except:
        logging.debug("No directories found in 'images/'")
        num_left_off = 0
    logging.debug(f"Starting from pokemon #{num_left_off+1}")

    conn = sqlite3.connect("pokedex.db")
    cur = conn.cursor()
    logging.debug(f"Using batch size={batch_size}")

    query = f"SELECT name, gen, num FROM pokemon WHERE gen > 0 AND gen <= 6 AND forme IS NULL AND num > {num_left_off} AND num <= {num_left_off + batch_size}"

    logging.debug(f"Running query: {query}")
    result = cur.execute(query).fetchall()

    forms = ["normal", "back"]
    generations = {
        1 : ["yellow", "red-blue"],
        2 : ["crystal", "gold", "silver"],
        3 : ["emerald", "firered-leafgreen", "ruby-sapphire"],
        4 : ["heartgold-soulsilver", "platinum", "diamond-pearl"],
        5 : ["black-white"],
        6 : ["bank", "go", "x-y"]
    }

    for t in result:
        name = t[0]
        gen = t[1]
        num = t[2]
        logging.debug(f"Starting to fetch {name}")
        start = time.time()
        for g in range(6, gen-1, -1):
            for source in generations[g]:
                for form in forms:
                    if not os.path.exists(f"images/{num}_{name.lower()}"):
                        logging.debug(f"Making directory: images/{num}_{name.lower()}")
                        os.mkdir(f"images/{num}_{name.lower()}")

                    r = requests.get(f"{base_url}/{source}/{form}/{name.lower()}.png")
                    if r.status_code == 200:
                        logging.debug(f"Adding images/{num}_{name.lower()}/{source}-{form}.png")
                        with open(f"images/{num}_{name.lower()}/{source}-{form}.png", "wb") as f:
                            f.write(r.content)
                    else:
                        logging.error(f"Error fetching {base_url}/{source}/{form}/{name.lower()}.png, could be an error with generation, or sprite type")
                        continue
        end = time.time()
        logging.debug(f"Total time to fetch {name}: {end-start}s")