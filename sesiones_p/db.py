import sqlite3
import hashlib

# Conexión y creación de tabla
conn = sqlite3.connect("usuarios.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
)
""")

# Crear usuario admin (contraseña: 1234)
usuario = "admin"
password_plano = "1234"
password_hash = hashlib.sha256(password_plano.encode()).hexdigest()

try:
    c.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, password_hash))
    conn.commit()
    print("Usuario admin creado con contraseña '1234'")
except sqlite3.IntegrityError:
    print("Usuario admin ya existe")

conn.close()
