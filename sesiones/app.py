import web
import sqlite3
import hashlib
import os

# Desactivar debug para producción
web.config.debug = False

# Rutas
urls = (
    "/", "Index",
    "/login/", "Login",
    "/logout/", "Logout",
    "/register/", "Register"
)

# Crear la aplicación
app = web.application(urls, globals())

# Configuración de sesiones
if not os.path.exists("sessions"):
    os.mkdir("sessions")

session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"user": None})

# Conexión a la base de datos SQLite
def get_db():
    return sqlite3.connect("users.db")

# Crear tabla de usuarios si no existe
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    db.commit()

# Página principal
class Index:
    def GET(self):
        if not session.user:
            raise web.seeother("/login")
        return f"Bienvenido, {session.user} | <a href='/logout'>Cerrar sesión</a>"

# Registro de usuarios
class Register:
    def GET(self):
        return """
            <form method='POST'>
                Usuario: <input type='text' name='username'><br>
                Contraseña: <input type='password' name='password'><br>
                <input type='submit' value='Registrarse'>
            </form>
        """

    def POST(self):
        data = web.input()
        username = data.username
        password = hashlib.sha256(data.password.encode()).hexdigest()

        try:
            with get_db() as db:
                db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                db.commit()
            return "Usuario registrado correctamente. <a href='/login'>Iniciar sesión</a>"
        except sqlite3.IntegrityError:
            return "El usuario ya existe."

# Inicio de sesión
class Login:
    def GET(self):
        return """
            <form method='POST'>
                Usuario: <input type='text' name='username'><br>
                Contraseña: <input type='password' name='password'><br>
                <input type='submit' value='Iniciar sesión'>
            </form>
        """

    def POST(self):
        data = web.input()
        username = data.username
        password = hashlib.sha256(data.password.encode()).hexdigest()

        with get_db() as db:
            cur = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()

        if user:
            session.user = username
            raise web.seeother("/")
        else:
            return "Usuario o contraseña incorrectos."

# Cerrar sesión
class Logout:
    def GET(self):
        session.user = None
        raise web.seeother("/login")

if __name__ == "__main__":
    app.run()
