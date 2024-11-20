use rusqlite::{Connection, Result};

fn run_query(conn: &Connection, q: &str) -> Result<Vec<String>> {
    let mut stmt = conn.prepare(q)?;
    let mut rows = stmt.query([])?;

    let mut names = Vec::new();
    while let Some(row) = rows.next()? {
        names.push(row.get(0)?);
    }

    Ok(names)
}

fn main() -> Result<()> {
    let conn: Connection = Connection::open("./pokedex.db")?;
    let query = "SELECT name FROM pokemon WHERE ability1 = 'Chlorophyll' OR ability2 = 'Chlorophyll' OR abilityh = 'Chlorophyll'";
    let names: Vec<String> = run_query(&conn, query)?;

    for name in names {
        println!("{}", name);
    }

    Ok(())
}