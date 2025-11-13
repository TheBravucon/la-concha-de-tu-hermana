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

def obtener_productos():
    conexion = conectar()
    productos = conexion.execute('SELECT id, descripcion, precio, cantidad FROM products').fetchall()
    conexion.close()
    return productos

def guardar_producto(nombre, precio, cantidad, editando=False, producto_id=None):
    conexion = conectar()
    if editando and producto_id:
        conexion.execute(
            'UPDATE products SET descripcion=?, precio=?, cantidad=? WHERE id=?',
            (nombre, precio, cantidad, producto_id)
        )
    else:
        conexion.execute(
            'INSERT INTO products (descripcion, precio, cantidad) VALUES (?, ?, ?)',
            (nombre, precio, cantidad)
        )
    conexion.commit()
    conexion.close()

def borrar_producto(producto_id):
    conexion = conectar()
    conexion.execute('DELETE FROM products WHERE id=?', (producto_id,))
    conexion.commit()
    conexion.close()

def buscar_productos(termino):
    conexion = conectar()
    query = '''SELECT id, descripcion, precio, cantidad FROM products
               WHERE descripcion LIKE '%' || ? || '%' OR id = ?'''
    productos = conexion.execute(query, (termino, termino)).fetchall()
    conexion.close()
    return productos
