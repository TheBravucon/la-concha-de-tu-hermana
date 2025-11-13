import hashlib
import sqlite3
from enum import Enum

DB_NAME = "inventario.db"

Rol = Enum('Rol', [('cliente', 1), ('proveedor', 2)])


def validar_rol(rol):
    if not getattr(Rol, rol):
        return 'Rol inválido'

    return None


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tabla_usuarios():
    conexion = conectar()
    conexion.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT CHECK(rol IN ('cliente', 'proveedor')) NOT NULL
    )''')
    conexion.commit()
    conexion.close()


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def registrar_usuario(nombre, email, password, rol):
    msg = validar_rol(rol)
    if msg is not None:
        return False, msg

    conexion = conectar()
    try:
        conexion.execute('INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, ?)',
                         (nombre, email, hash_password(password), rol))
        conexion.commit()
        return True, "Usuario registrado correctamente"
    except sqlite3.IntegrityError:
        return False, "El correo ya está registrado"
    finally:
        conexion.close()


def verificar_login(email, password):
    conexion = conectar()
    cursor = conexion.execute('SELECT id, nombre, rol, password FROM usuarios WHERE email=?', (email,))
    user = cursor.fetchone()
    conexion.close()
    if user and user[3] == hash_password(password):
        return True, {"id": user[0], "nombre": user[1], "rol": user[2]}
    else:
        return False, "Correo o contraseña incorrectos"


def obtener_usuarios():
    conexion = conectar()
    data = conexion.execute('SELECT id, nombre, email, rol FROM usuarios').fetchall()
    conexion.close()
    return data


def eliminar_usuario(user_id):
    conexion = conectar()
    conexion.execute('DELETE FROM usuarios WHERE id=?', (user_id,))
    conexion.commit()
    conexion.close()
