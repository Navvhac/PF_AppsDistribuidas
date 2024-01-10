from flask import Flask, request, jsonify, send_file, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from tkinter import Tk, filedialog
from werkzeug.security import generate_password_hash, check_password_hash
import os, re,json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'areshr'

DB_PATH = 'database.json'

#Instancia de LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'mostrar_login'

#FUNCIONES PARA REGISTRO DE USUARIOS 
class User(UserMixin):
    def __init__(self, id, username, password,correo):
        self.id = id
        self.username = username
        self.password = password
        self.correo = correo
        
def cargar_usuarios():
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
        with open(DB_PATH, 'r') as file:
            usuarios = json.load(file)
        return {int(user_id): User(int(user_id), user['username'], user['password'], user['correo']) for user_id, user in usuarios.items()}
    return {}

# Guardar usuarios en el archivo JSON
def guardar_usuarios(usuarios):
    usuarios_data = {str(user.id): {'username': user.username, 'password': user.password, 'correo': user.correo} for user in usuarios.values()}
    with open(DB_PATH, 'w') as file:
        json.dump(usuarios_data, file, indent=4)

usuarios_db = cargar_usuarios()

#función para cargar un usuario a partir de su ID de usuario
@login_manager.user_loader  
def load_user(user_id):
    return usuarios_db.get(int(user_id))
         
# RUTAS PARA ADMINISTRACIÓN DE USUARIOS
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        correo = request.form.get('correo')

        if not username or not password or not correo:
            flash('Por favor, completa todos los campos.', 'error')
            return redirect(url_for('registrar'))

        if any(user.username == username for user in usuarios_db.values()):
            flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')
            return redirect(url_for('registrar'))

        nuevo_id = max(usuarios_db.keys(), default=0) + 1
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        nuevo_usuario = User(nuevo_id, username, hashed_password, correo)
        usuarios_db[nuevo_id] = nuevo_usuario
        guardar_usuarios(usuarios_db)

        login_user(nuevo_usuario)

        flash('¡Registro exitoso! Bienvenido, {}'.format(username), 'success')
        return redirect(url_for('main'))
    #Muestra el formulario de registro en la solicitud GET
    return render_template('registro.html')

# Ruta para manejar el formulario de login
@app.route('/login', methods=['GET', 'POST'])
def mostrar_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica si el usuario y la contraseña son 'admin'
        if username == 'admin' and password == 'admin':
            # Redirige a la ruta '/admin'
            return redirect(url_for('admin'))
        
        # Verificar la autenticación aquí usando la lógica de tu aplicación
        usuario = next((user for user in usuarios_db.values() if user.username == username), None)
            
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash('¡Login exitoso!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'error')

    return render_template('login.html')

#CODIGO INCOMPLETO 
#RUTA PARA PAGINA PRINCIPAL
@app.route('/main')
@login_required
def main():
    return render_template('main.html')

#RUTA PARA PAGINA DE ADMINISTRADOR DE DB
@app.route('/admin')
@login_required
def admin():
        return render_template('admin.html')
    
    
#FUNCIONES PARA CARGA Y DESCARGA DE ARCHIVOS

# Rutas para la transferencia de información, ruta para cargar
@app.route('/upload', methods=['POST'])
def cargar_archivo():
    try:
        # Verificar si se envió un archivo en la solicitud
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo en la solicitud'}), 400

        archivo = request.files['file']

        # Verificar si se seleccionó un archivo
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Crear el directorio de destino si no existe
        directorio_destino = './archivos_cargados'
        os.makedirs(directorio_destino, exist_ok=True)

        # Guardar el archivo en el servidor
        ruta_guardado = os.path.join(directorio_destino, archivo.filename)
        archivo.save(ruta_guardado)

        return jsonify({'mensaje': f'Archivo "{archivo.filename}" cargado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al cargar el archivo: {str(e)}'}), 500

#Ruta para descargar 
@app.route('/download/<nombre_archivo_servidor>', methods=['GET'])
def descargar_archivo(nombre_archivo_servidor):
    try:
        ruta_archivo = os.path.join('archivos_cargados', nombre_archivo_servidor)
        if os.path.exists(ruta_archivo):
            return send_file(ruta_archivo, as_attachment=True)
        return jsonify({'mensaje': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'mensaje': f'Error al descargar el archivo: {str(e)}'}), 500

#Servidor 
if __name__ == '__main__':
    app.run(debug=True)