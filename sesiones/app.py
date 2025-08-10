import web
import sqlite3
import hashlib

urls = (
    "/", "Index",
    "/login", "Login",
    "/logout", "Logout",
    "/administracion", "Administracion",
)

web.config.debug = False

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"))
render = web.template.render("templates/")

class Index:
    def GET(self):
        # Imprime los valores almacenados en la session.
        # NOTA: solo es para verificar visualmente los valores.
        print(f"logged_in: {session.get("logged_in")}")
        print(f"name: {session.get("name")}")

        # Valida si logged_in es True
        if session.get("logged_in"):
            # Renderiza la pagina index.html y le envia el nombre del usuario
            return render.index(session.get("name"))
        else:
            # Redirecciona a login
            raise web.seeother("/login")

class Administracion:
    def GET(self):
        # Imprime los valores almacenados en la session.
        # NOTA: solo es para verificar visualmente los valores.
        print(f"logged_in: {session.get("logged_in")}")
        print(f"name: {session.get("name")}")


        # Valida si logged_in es True
        if session.get("logged_in"):
            # Renderiza la pagina administracion.html y le envia el nombre del usuario
            return render.administracion(session.get("name"))
        else:
            raise web.seeother("/login")

class Login:
    def GET(self):
        if session.get("logged_in"):
            raise web.seeother("/")
        return render.login()

    def POST(self):
        # Almacena los datos del formulario de login.html
        formulario = web.input()
        username = formulario.username
        password = formulario.password
        # Imprime los datos solo para verificarlos visualmente
        print(f"username: {username}")
        print(f"password: {password}")

        # Codifica el password en UTF-8
        password_bytes = password.encode('utf-8')
        # Cifra el password en sha1, tal como esta almacenado en la base de datos
        password_sha1 = hashlib.sha1(password_bytes).hexdigest()

        # Crea una conexion con la base de datos
        conn = sqlite3.connect('base_demo.db')
        # Crea un cursor para realizar las consultas
        c = conn.cursor()

        # Prepara la sentencia de consulta para prevenir inyeccion de sql.
        sql = "SELECT username,name FROM users WHERE username=? AND password=?"
        # datos de la consulta con el password cifrado
        data = (username,password_sha1)
        # Ejecuta la consulta
        c.execute(sql,data)
        # Obtiene el registro en caso de que el username y el password coincidan en la consulta.
        result = c.fetchone()
        # Imprimir el username para verificar
        # NOTA: en caso de que el username o el password no coincidan imprimira None.
        print(f"Resultado consulta: {result}")
        # Si la consulta es distinta a None existe un usuario con esos datos.
        if result is not None:
            session.logged_in = True # Indica que la sesion fue iniciada
            session.name = result[1] # Alamcena el segundo elemento de conjunto, en este caso "name"
            raise web.seeother("/")
        else:
            # En caso de que no haya un registro con esos datos renderiza login y envia un mensaje
            return render.login("El nombre de usuario o contraseña son incorrectos")

class Logout:
    def GET(self):
        # Cierra la session
        session.kill()
        # Redirecciona a login.html
        raise web.seeother("/login")

if __name__ == "__main__":
    app.run()