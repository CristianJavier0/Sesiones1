import sqlite3
import hashlib
from datetime import datetime

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Crear tabla Rol (sin cambios)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rol (
        id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_rol TEXT NOT NULL
    )
    ''')
    
    # Crear tabla Usuarios (sin cambios)
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
    
    # Nueva tabla de sesiones con los campos requeridos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        session_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_activity TIMESTAMP,
        expires_at TIMESTAMP,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
    )
    ''')
    
    # Insertar roles por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM Rol")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Rol (nombre_rol) VALUES ('admin')")
        cursor.execute("INSERT INTO Rol (nombre_rol) VALUES ('usuario')")
    
    # Crear usuario admin de prueba si no existe
    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE correo_U = 'admin@example.com'")
    if cursor.fetchone()[0] == 0:
        hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
        INSERT INTO Usuarios (
            nombre_U, apellido_PU, apellido_MU, fecha_registro_U, 
            correo_U, contrasena, id_rol
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Admin', 'Sistema', '', datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'admin@example.com', hashed_password, 1  # id_rol 1 = admin
        ))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def register_user(nombre, apellido_p, apellido_m, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO Usuarios (
            nombre_U, apellido_PU, apellido_MU, fecha_registro_U, 
            correo_U, contrasena, id_rol
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            nombre, apellido_p, apellido_m, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            email, hashed_password, 2  # id_rol 2 = usuario normal
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # Email ya existe
        return False
    finally:
        conn.close()

def verify_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT u.*, r.nombre_rol 
    FROM Usuarios u 
    JOIN Rol r ON u.id_rol = r.id_rol 
    WHERE u.correo_U = ? AND u.contrasena = ?
    ''', (email, hashed_password))
    
    user = cursor.fetchone()
    conn.close()
    return user

def start_session(user_id, session_id, ip_address, user_agent, expires_at):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO user_sessions (
        session_id, user_id, ip_address, user_agent, 
        last_activity, expires_at, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        session_id, user_id, ip_address, user_agent,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expires_at, 1
    ))
    
    conn.commit()
    conn.close()

def update_session_activity(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE user_sessions 
    SET last_activity = ?
    WHERE session_id = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), session_id))
    
    conn.commit()
    conn.close()

def end_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE user_sessions 
    SET is_active = 0
    WHERE session_id = ?
    ''', (session_id,))
    
    conn.commit()
    conn.close()

def get_active_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT us.*, u.nombre_U, u.apellido_PU
    FROM user_sessions us
    JOIN Usuarios u ON us.user_id = u.id_usuario
    WHERE us.is_active = 1
    ''')
    
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM user_sessions WHERE session_id = ?
    ''', (session_id,))
    
    session = cursor.fetchone()
    conn.close()
    return session

create_tables()  # Crear tablas al iniciar el módulo