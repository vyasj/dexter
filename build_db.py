import json
import sqlite3
import logging


def val_if_exists(data, key):
    try:
        return data[key]
    except:
        return None
    

def calc_gen(natdex_num, forme_name):
    if forme_name is not None:
        if "paldea" in forme_name.lower():
            return 9
        elif "gmax" in forme_name.lower() or "hisui" in forme_name.lower() or "galar" in forme_name.lower():
            return 8
        elif "alola" in forme_name.lower():
            return 7
        elif "mega" in forme_name.lower():
            return 6
        else:
            logging.error(f"unknown forme type '{forme_name.lower()}' for pokemon #{natdex_num}")
            return 0
    else:
        if natdex_num >= 906 and natdex_num <= 1025:
            return 9
        elif natdex_num >= 810 and natdex_num <= 905:
            return 8
        elif natdex_num >= 722 and natdex_num <= 809:
            return 7
        elif natdex_num >= 650 and natdex_num <= 721:
            return 6
        elif natdex_num >= 494 and natdex_num <= 649:
            return 5
        elif natdex_num >= 387 and natdex_num <= 493:
            return 4
        elif natdex_num >= 252 and natdex_num <= 386:
            return 3
        elif natdex_num >= 152 and natdex_num <= 251:
            return 2
        elif natdex_num >= 1 and natdex_num <= 151:
            return 1
        else:
            logging.error(f"could not determine generation for pokemon #{natdex_num} forme={forme_name}")
            return 0


def create():
    logging.debug("Creating database with table")

    conn = sqlite3.connect('pokedex.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 
                pokemon(num, 
                name, 
                gen, 
                base_species, 
                forme, 
                type1, 
                type2, 
                base_hp, 
                base_atk, 
                base_spa, 
                base_def, 
                base_spd, 
                base_spe, 
                ability1, 
                ability2, 
                abilityh, 
                prevo, 
                evo1, 
                evo2, 
                evo3
                )""")
    conn.commit()
    conn.close()



def populate():
    logging.debug("Populating table with data from json file")

    data = json.load(open("pokedex.json"))
    conn = sqlite3.connect('pokedex.db')
    cur = conn.cursor()

    for key in data.keys():
        is_nonstandard = val_if_exists(data[key], 'isNonstandard')
        
        if is_nonstandard == 'Custom' or is_nonstandard == 'CAP':
            logging.debug(f'Skipping {key}')
            continue
        logging.debug(f"Inserting {key} into table")

        num = data[key]['num']
        name = data[key]['name']
        base_species = val_if_exists(data[key], 'baseSpecies')
        forme = val_if_exists(data[key], 'forme')
        gen = calc_gen(num, forme)
        type1 = data[key]['types'][0]
        type2 = val_if_exists(data[key]['types'], 1)
        base_hp = data[key]['baseStats']['hp']
        base_atk = data[key]['baseStats']['atk']
        base_spa = data[key]['baseStats']['spa']
        base_def = data[key]['baseStats']['def']
        base_spd = data[key]['baseStats']['spd']
        base_spe = data[key]['baseStats']['spe']
        ability1 = data[key]['abilities']['0']
        ability2 = val_if_exists(data[key]['abilities'], ['1'])
        abilityh = val_if_exists(data[key]['abilities'], 'H')
        prevo = val_if_exists(data[key], 'prevo')
        evos = val_if_exists(data[key], 'evos')
        evo1 = val_if_exists(evos, 0)
        evo2 = val_if_exists(evos, 1)
        evo3 = val_if_exists(evos, 2)
        
        params = (num, name, gen, base_species, forme, type1, type2, base_hp, base_atk, base_spa, base_def, base_spd, base_spe, ability1, ability2, abilityh, prevo, evo1, evo2, evo3)
        
        cur.execute(f"""
            INSERT INTO pokemon VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, params)

        conn.commit()

    conn.close()