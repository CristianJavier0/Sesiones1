from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import secrets
import os
from sql.db import DatabaseHandler

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Inicializar el manejador de la base de datos
db = DatabaseHandler()

# Rutas de la aplicación
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        
        if db.create_user(username, password, email):
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('El nombre de usuario o email ya está en uso.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.verify_user(username, password)
        
        if user:
            # Crear nueva sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['session_id'] = secrets.token_hex(16)
            
            # Registrar sesión en la base de datos
            db.log_session(
                user_id=user['id'],
                session_id=session['session_id'],
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Actualizar actividad de la sesión
    if 'session_id' in session:
        db.update_session_activity(session['session_id'])
    
    # Obtener sesiones activas del usuario
    active_sessions = db.get_active_sessions(session['user_id'])
    
    return render_template('dashboard.html', 
                          username=session['username'],
                          active_sessions=active_sessions)

@app.route('/logout')
def logout():
    if 'session_id' in session:
        db.invalidate_session(session['session_id'])
    
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/sessions')
def admin_sessions():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Aquí podrías verificar si el usuario es administrador
    all_sessions = db.get_active_sessions()
    return render_template('admin_sessions.html', active_sessions=all_sessions)

if __name__ == '__main__':
    app.run(debug=True)