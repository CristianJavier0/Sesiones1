from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import get_session, update_session_activity, verify_user, register_user, start_session, end_session, get_active_sessions
import functools
from datetime import datetime, timedelta
from flask import session
import hashlib

app = Flask(__name__)
app.secret_key = '15'
app.permanent_session_lifetime = timedelta(minutes=30)  # Sesión expira en 30 minutos

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = verify_user(email, password)
        
        if user:
            # Crear información de la sesión
            session.permanent = True
            session_id = session.sid
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            expires_at = (datetime.now() + app.permanent_session_lifetime).strftime("%Y-%m-%d %H:%M:%S")
            
            # Registrar en base de datos
            start_session(
                user['id_usuario'], 
                session_id, 
                ip_address, 
                user_agent, 
                expires_at
            )
            
            # Configurar sesión Flask
            session['user_id'] = user['id_usuario']
            session['user_email'] = user['correo_U']
            session['user_name'] = user['nombre_U']
            session['user_role'] = user['nombre_rol']
            
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
        else:
            success = register_user(nombre, apellido_p, apellido_m, email, password)
            if success:
                flash('Registro exitoso! Ahora puedes iniciar sesión', 'success')
                return redirect(url_for('login'))
            else:
                flash('El correo electrónico ya está registrado', 'danger')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    active_sessions = []
    if session['user_role'] == 'admin':
        active_sessions = get_active_sessions()
    
    return render_template('dashboard.html', 
                         user_name=session['user_name'],
                         user_role=session['user_role'],
                         active_sessions=active_sessions)

@app.route('/logout')
@login_required
def logout():
    if 'session_id' in session:
        end_session(session['session_id'])
    
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('login'))

@app.before_request
def update_last_activity():
    if 'user_id' in session:
        # Generar un ID de sesión único basado en la sesión actual
        session_data = str(session.get('_id', '')) + str(session.get('user_id', ''))
        session_id = hashlib.sha256(session_data.encode()).hexdigest()
        
        # Verificar si esta sesión ya está registrada en la base de datos
        db_session = get_session(session_id)
        if db_session:
            update_session_activity(session_id)

if __name__ == '__main__':
    app.run(debug=True)