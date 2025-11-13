import sqlite3

DB_NAME = "inventario.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    conexion = conectar()
    query = '''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL
    )'''
    conexion.execute(query)
    conexion.commit()
    conexion.close()


def obtener_producto_by_id(id):
    conexion = conectar()
    producto = conexion.execute('SELECT id, descripcion, precio, cantidad FROM products where id = ?', (id,)).fetchone()
    conexion.close()
    return producto


def obtener_productos():
    conexion = conectar()
    productos = conexion.execute('SELECT id, descripcion, precio, cantidad FROM products').fetchall()
    conexion.close()
    return productos


def guardar_producto(nombre, precio, cantidad, editando=False, producto_id=None):
    conexion = conectar()
    if editando and producto_id:
        rows_affected = conexion.execute(
            'UPDATE products SET descripcion=?, precio=?, cantidad=? WHERE id=?',
            (nombre, precio, cantidad, producto_id)
        ).rowcount
    else:
        rows_affected = conexion.execute(
            'INSERT INTO products (descripcion, precio, cantidad) VALUES (?, ?, ?)',
            (nombre, precio, cantidad)
        ).rowcount
    conexion.commit()
    conexion.close()
    return rows_affected


def borrar_producto(producto_id):
    conexion = conectar()
    rows_affected = conexion.execute('DELETE FROM products WHERE id=?', (producto_id,)).rowcount
    conexion.commit()
    conexion.close()
    return rows_affected


def buscar_productos(termino):
    conexion = conectar()
    query = '''SELECT id, descripcion, precio, cantidad FROM products
               WHERE descripcion LIKE '%' || ? || '%' OR id = ?'''
    productos = conexion.execute(query, (termino, termino)).fetchall()
    conexion.close()
    return productos


def actualizar_stock(id, stock):
    conexion = conectar()
    query = '''update products set cantidad = cantidad - ? where id = ?'''
    conexion.execute(query, (stock, id))
    conexion.commit()
    conexion.close()
