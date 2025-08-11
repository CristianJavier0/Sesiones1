import web
import sqlite3
import hashlib

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/administracion', 'Administracion'
)

app = web.application(urls, globals())

web.config.debug = False
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'usuario': None})

render = web.template.render('templates/')

def get_db():
    return sqlite3.connect("usuarios.db")

class Index:
    def GET(self):
        print(f"logged_in: {session.get('logged_in')}")
        print("Sesión actual:", dict(session))  # Debug
        usuario = session.get('usuario')
        return render.index(usuario=usuario)
    
class Login:
    def GET(self):
        print("Accediendo a la página de login")
        print("Sesión actual:", dict(session))  # Debug
        return render.login(usuario="")

    def POST(self):
        data = web.input()
        usuario = data.usuario
        contrasena = hashlib.sha256(data.contrasena.encode()).hexdigest()

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?", (usuario, contrasena))
        user = c.fetchone()
        conn.close()

        if user:
            session.usuario = usuario
            session.logged_in = True
            print(f"logged_in: {session.get('logged_in')}")
            print(f"usuario: {session.get('usuario')}")
            print("Sesión después de login:", dict(session))  # Debug
            return render.index(usuario=usuario)
        else:
            return render.login(usuario="")

class Administracion:
    def GET(self):
        try:
            usuario = session.get('usuario')
            if not usuario:
                print("Redirigiendo a login: sesión no encontrada")
                return render.login(usuario="")
            else:
                print(f"Sesión encontrada: {dict(session)}")
                print(f"Acceso concedido a administración para {usuario}")
                return render.administracion(usuario=usuario)
            
        except Exception as e:
            print(f"Error en Administracion.GET: {e}")
            return render.index(usuario="")

class Logout:
    def GET(self):
        session.usuario = None
        session.logged_in = False
        print("Sesión cerrada. Redirigiendo a index.")
        return render.index(usuario="")
    
if __name__ == "__main__":
    app.run()
