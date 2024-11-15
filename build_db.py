import json
import sqlite3

if __name__ == "__main__":
    data = json.load(open("pokedex.json"))

    conn = sqlite3.connect('pokedex.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE pokemon(num, name, type1, type2, base_hp, base_atk, base_spa, base_def, base_spd, base_spe, ability1, ability2, abilityh, prevo, evo1, evo2, evo3)')

    for key in data.keys():
        try:
            is_nonstandard = data[key]['isNonstandard']
        except:
            is_nonstandard = None
        
        if is_nonstandard == 'Custom' or is_nonstandard == 'CAP':
            print(f'skipping {key}')
            continue

        print(f'adding {key}')
        name = key
        num = data[name]['num']
        type1 = data[name]['types'][0]
        type2 = None if len(data[name]['types']) == 1 else data[name]['types'][1]
        base_hp = data[name]['baseStats']['hp']
        base_atk = data[name]['baseStats']['atk']
        base_spa = data[name]['baseStats']['spa']
        base_def = data[name]['baseStats']['def']
        base_spd = data[name]['baseStats']['spd']
        base_spe = data[name]['baseStats']['spe']
        ability1 = data[name]['abilities']['0']
        try:
            ability2 = data[name]['abilities']['1']
        except:
            ability2 = None
        try:
            abilityh = data[name]['abilities']['H']
        except:
            abilityh = None
        try:
            prevo = data[name]['prevo']
        except:
            prevo = None
        try:
            evo1 = data[name]['evos'][0]
        except:
            evo1 = None
        try:
            evo2 = data[name]['evos'][1]
        except:
            evo2 = None
        try:
            evo3 = data[name]['evos'][2]
        except:
            evo3 = None
        
        params = (num, name, type1, type2, base_hp, base_atk, base_spa, base_def, base_spd, base_spe, ability1, ability2, abilityh, prevo, evo1, evo2, evo3)
        
        cur.execute(f"""
            INSERT INTO pokemon VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, params)

        conn.commit()

    print(cur.execute("""SELECT * FROM pokemon WHERE ability1 = 'Chlorophyll'""").fetchall())