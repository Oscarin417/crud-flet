import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conex = mysql.connector.connect(
                host=os.environ.get("DATABASE_HOST"),
                user=os.environ.get("DATABASE_USER"),
                password=os.environ.get("DATABASE_PASSWORD"),
                database=os.environ.get("DATABASE_NAME")
            )

    return conex

def fetch_all_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, cantidad FROM productos ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_producto(prod_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, cantidad FROM productos WHERE id = %s", (prod_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def insert_producto(nombre:str, precio:float, cantidad:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)",
        (nombre, precio, cantidad)
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_producto(id_:int, nombre:str, precio:float, cantidad:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
        (nombre, precio, cantidad, id_)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_producto(id_:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id_,))
    conn.commit()
    cursor.close()
    conn.close()
