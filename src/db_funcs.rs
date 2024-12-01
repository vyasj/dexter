use rusqlite::{Connection, Result};

pub fn connect(filename: &str) -> Result<Connection> {
    let conn: Connection = Connection::open(filename)?;

    Ok(conn)
}

pub fn run_query(conn: &Connection, q: &str) -> Result<Vec<String>> {
    let mut stmt = conn.prepare(q)?;
    let mut rows = stmt.query([])?;

    let mut names = Vec::new();
    while let Some(row) = rows.next()? {
        names.push(row.get(0)?);
    }

    Ok(names)
}