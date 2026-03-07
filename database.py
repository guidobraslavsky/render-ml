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
        estado TEXT DEFAULT 'pendiente',
        printed INTEGER DEFAULT 0
    )
"""
    )

    conn.commit()
    conn.close()


def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


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


def get_orders_pending_print():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT pedido_ml as order_id
        FROM reclamos
        WHERE printed = 0
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return [{"order_id": r["order_id"]} for r in rows]


def mark_order_printed(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reclamos
        SET printed = 1
        WHERE pedido_ml = ?
    """,
        (order_id,),
    )

    conn.commit()
    conn.close()


def insert_order(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reclamos (pedido_ml, printed)
        VALUES (?,0)
        """,
        (order_id,),
    )

    conn.commit()
    conn.close()


def order_exists(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM reclamos WHERE pedido_ml = ?", (order_id,))

    result = cursor.fetchone()

    conn.close()

    return result is not None
