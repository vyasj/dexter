mod db_funcs;

fn main() {
    let db_name = "./pokedex.db";
    let query = "SELECT name FROM pokemon WHERE forme IS NULL AND gen = 1";

    let cnxn = db_funcs::connect(db_name).unwrap();
    let names = db_funcs::run_query(&cnxn, query).unwrap();

    for name in names {
        println!("{}", name);
    }
}