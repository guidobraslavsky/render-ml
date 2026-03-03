import sqlite3

DB_NAME = "reclamos.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reclamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            nombre TEXT,
            pedido_ml TEXT,
            contacto TEXT,
            producto TEXT,
            tipo TEXT,
            descripcion TEXT,
            estado TEXT DEFAULT 'pendiente'
        )
    """
    )

    conn.commit()
    conn.close()


def guardar_reclamo(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reclamos (nombre, pedido_ml, contacto, producto, tipo, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            data.get("nombre"),
            data.get("pedido_ml"),
            data.get("contacto"),
            data.get("producto"),
            data.get("tipo"),
            data.get("descripcion"),
        ),
    )

    reclamo_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return reclamo_id
