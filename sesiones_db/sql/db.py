import sqlite3
from datetime import datetime, timedelta
import hashlib
import secrets
import os

class DatabaseHandler:
    def __init__(self, db_path='sessions.db'):
        """Inicializa el manejador de la base de datos"""
        # Obtener el directorio donde está este archivo (sql/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Ruta completa de la base de datos
        self.db_path = os.path.join(current_dir, db_path)
        
        self._initialize_db()
        self._verify_tables()
    
    def _initialize_db(self):
        """Intenta crear la base de datos"""
        try:
            # Conexión para crear el archivo si no existe
            conn = sqlite3.connect(self.db_path)
            conn.close()
            print(f"Base de datos creada en: {self.db_path}")
        except Exception as e:
            print(f"Error al crear la base de datos: {e}")
            raise
    
    def _verify_tables(self):
        """Verifica y crea las tablas necesarias"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar tablas existentes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = {row[0] for row in cursor.fetchall()}
            
            # Crear tabla users si no existe
            if 'users' not in existing_tables:
                cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
                print("Tabla 'users' creada")
            
            # Crear tabla user_sessions si no existe
            if 'user_sessions' not in existing_tables:
                cursor.execute('''
                CREATE TABLE user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')
                print("Tabla 'user_sessions' creada")
            
            conn.commit()
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @staticmethod
    def _hash_password(password, salt=None):
        """Genera un hash seguro de la contraseña"""
        if salt is None:
            salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return password_hash, salt
    
    def create_user(self, username, password, email=None):
        """Crea un nuevo usuario en la base de datos"""
        password_hash, salt = self._hash_password(password)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO users (username, password_hash, salt, email)
                VALUES (?, ?, ?, ?)
                ''', (username, password_hash, salt, email))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al crear usuario: {e}")
            return False
    
    def verify_user(self, username, password):
        """Verifica las credenciales del usuario"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, username, password_hash, salt FROM users 
            WHERE username = ?
            ''', (username,))
            user = cursor.fetchone()
        
        if user:
            password_hash, _ = self._hash_password(password, user['salt'])
            if password_hash == user['password_hash']:
                return {'id': user['id'], 'username': user['username']}
        return None
    
    def log_session(self, user_id, session_id, ip, user_agent):
        """Registra una nueva sesión de usuario"""
        expires_at = datetime.now() + timedelta(hours=1)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO user_sessions (session_id, user_id, ip_address, user_agent, last_activity, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, user_id, ip, user_agent, datetime.now(), expires_at))
            conn.commit()
    
    def update_session_activity(self, session_id):
        """Actualiza la actividad de una sesión"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE user_sessions 
            SET last_activity = ?, expires_at = ?
            WHERE session_id = ? AND is_active = 1
            ''', (datetime.now(), datetime.now() + timedelta(hours=1), session_id))
            conn.commit()
    
    def invalidate_session(self, session_id):
        """Invalida una sesión específica"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE user_sessions 
            SET is_active = 0 
            WHERE session_id = ?
            ''', (session_id,))
            conn.commit()
    
    def get_active_sessions(self, user_id=None):
        """Obtiene sesiones activas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute('''
                SELECT * FROM user_sessions 
                WHERE user_id = ? AND is_active = 1 AND expires_at > ?
                ORDER BY last_activity DESC
                ''', (user_id, datetime.now()))
            else:
                cursor.execute('''
                SELECT * FROM user_sessions 
                WHERE is_active = 1 AND expires_at > ?
                ORDER BY last_activity DESC
                ''', (datetime.now(),))
            return cursor.fetchall()

# Prueba de funcionamiento
if __name__ == '__main__':
    print("=== Probando conexión a la base de datos ===")
    try:
        db = DatabaseHandler()
        print("✔ Base de datos inicializada correctamente")
        
        if db.create_user('admin', 'admin123'):
            print("✔ Usuario de prueba creado")
        else:
            print("✖ El usuario de prueba ya existe")
            
        user = db.verify_user('admin', 'admin123')
        if user:
            print(f"✔ Usuario verificado: {user['username']}")
        else:
            print("✖ Error al verificar usuario")
            
    except Exception as e:
        print(f"✖ Error durante la prueba: {e}")
