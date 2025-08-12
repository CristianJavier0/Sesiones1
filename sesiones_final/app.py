from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto en producción

# Configuración de la base de datos
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Crear tabla Rol si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rol (
            id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_rol TEXT NOT NULL
        )
        ''')
        
        # Crear tabla Usuarios si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_U TEXT NOT NULL,
            apellido_PU TEXT NOT NULL,
            apellido_MU TEXT,
            fecha_registro_U TEXT NOT NULL,
            correo_U TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            id_rol INTEGER,
            FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
        )
        ''')
        
        # Crear tabla para monitorear sesiones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sesiones (
            id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_ultima_actividad TEXT NOT NULL,
            direccion_ip TEXT,
            user_agent TEXT,
            activa INTEGER DEFAULT 1,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        )
        ''')
        
        # Insertar roles básicos si no existen
        cursor.execute("SELECT COUNT(*) FROM Rol")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Rol (nombre_rol) VALUES ('admin')")
            cursor.execute("INSERT INTO Rol (nombre_rol) VALUES ('usuario')")
        
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT u.*, r.nombre_rol 
        FROM Usuarios u 
        JOIN Rol r ON u.id_rol = r.id_rol 
        WHERE correo_U = ? AND contrasena = ?
        ''', (correo, hash_password(contrasena)))
        
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            # Registrar la sesión en la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO Sesiones 
            (id_usuario, fecha_inicio, fecha_ultima_actividad, direccion_ip, user_agent) 
            VALUES (?, ?, ?, ?, ?)
            ''', (
                usuario['id_usuario'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                request.remote_addr,
                request.user_agent.string
            ))
            
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Almacenar información del usuario en la sesión de Flask
            session['usuario'] = {
                'id': usuario['id_usuario'],
                'nombre': f"{usuario['nombre_U']} {usuario['apellido_PU']}",
                'correo': usuario['correo_U'],
                'rol': usuario['nombre_rol'],
                'sesion_id': session_id
            }
            
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    # Actualizar última actividad en la sesión
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE Sesiones 
    SET fecha_ultima_actividad = ?
    WHERE id_sesion = ?
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), session['usuario']['sesion_id']))
    
    conn.commit()
    conn.close()
    
    # Obtener información de sesiones activas
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT s.*, u.nombre_U, u.apellido_PU 
    FROM Sesiones s
    JOIN Usuarios u ON s.id_usuario = u.id_usuario
    WHERE s.activa = 1 AND u.id_usuario = ?
    ''', (session['usuario']['id'],))
    
    sesiones_activas = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', usuario=session['usuario'], sesiones=sesiones_activas)

@app.route('/logout')
def logout():
    if 'usuario' in session:
        # Marcar la sesión como inactiva en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE Sesiones 
        SET activa = 0 
        WHERE id_sesion = ?
        ''', (session['usuario']['sesion_id'],))
        
        conn.commit()
        conn.close()
        
        # Eliminar la sesión de Flask
        session.pop('usuario', None)
        flash('Has cerrado sesión correctamente', 'success')
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)