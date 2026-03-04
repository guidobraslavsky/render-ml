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


def obtener_reclamos():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM reclamos
        ORDER BY fecha DESC
    """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def marcar_resuelto(reclamo_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reclamos
        SET estado = 'resuelto'
        WHERE id = ?
    """,
        (reclamo_id,),
    )

    conn.commit()
    conn.close()


def obtener_reclamo(reclamo_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reclamos WHERE id = ?", (reclamo_id,))

    reclamo = cursor.fetchone()

    conn.close()

    return reclamo
