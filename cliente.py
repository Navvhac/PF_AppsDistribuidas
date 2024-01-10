import os,requests,json
import tkinter as tk
from tkinter import filedialog

def mostrar_menu():
    print("Menú:")
    print("1. Cargar Archivo")
    print("2. Descargar Archivo")
    print("3. Ver Reportes")
    print("4. Gestionar Usuarios")
    print("5. Registrar Usuario")
    print("6. Iniciar Sesión")
    print("7. Listar Catálogo de Contenido")
    print("8. Gestionar Pagos")
    print("9. Ver Estadísticas")
    print("0. Salir")

def cargar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    ruta_archivo = filedialog.askopenfilename()  # Abre un cuadro de diálogo para seleccionar un archivo
    if ruta_archivo:
        url = 'http://localhost:5000/upload'
        archivos = {'file': open(ruta_archivo, 'rb')}
        respuesta = requests.post(url, files=archivos)
        print(respuesta.json())

def descargar_archivo():
    try:
        # Abre un cuadro de diálogo para seleccionar el archivo a descargar
        archivo_seleccionado = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(), 'archivos_cargados'),
            title="Selecciona el archivo a descargar",
            filetypes=[("Todos los archivos", "*.*")],
        )

        if archivo_seleccionado:
            # Obtiene el nombre del archivo del usuario
            nombre_archivo_servidor = os.path.basename(archivo_seleccionado)

            # Construye la URL completa para descargar el archivo seleccionado
            url_descarga = f'http://localhost:5000/download/{nombre_archivo_servidor}'

            # Realiza la solicitud GET para descargar el archivo
            respuesta_descarga = requests.get(url_descarga)

            if respuesta_descarga.status_code == 200:
                # Construye la carpeta de destino (archivos_descargados) si no existe
                directorio_destino = './archivos_descargados'
                os.makedirs(directorio_destino, exist_ok=True)

                # Guarda el archivo en la carpeta de destino
                ruta_descarga = os.path.join(directorio_destino, nombre_archivo_servidor)
                with open(ruta_descarga, 'wb') as f:
                    f.write(respuesta_descarga.content)

                print(f'Archivo descargado y guardado en "{ruta_descarga}"')
            else:
                print(f'Error al descargar el archivo. Código de estado: {respuesta_descarga.status_code}')
        else:
            print("Descarga cancelada o sin archivo seleccionado.")
    except Exception as e:
        print(f'Error en la descarga del archivo: {str(e)}')


def ver_reportes():
    # Lógica para mostrar reportes
    print("Acción: Ver Reportes")

def gestionar_usuarios():
    # Lógica para gestionar usuarios
    print("Acción: Gestionar Usuarios")

def registrar_usuario():
    username = input("Ingresa el nombre de usuario: ")
    password = input("Ingresa la contraseña: ")

    # Enviar datos al servidor como JSON
    data = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    # Realiza la solicitud POST para registrar al usuario
    respuesta_registro = requests.post(f'{servidor_url}/registro', data=json.dumps(data), headers=headers)

    # Analiza la respuesta del servidor
    respuesta_json = respuesta_registro.json()
    if respuesta_json['success']:
        print(respuesta_json['message'])
        # Aquí podrías realizar acciones adicionales después de un registro exitoso
    else:
        print(f'Error en el registro: {respuesta_json["message"]}')

def iniciar_sesion():
    # Lógica para iniciar sesión
    print("Acción: Iniciar Sesión")

def listar_catalogo_contenido():
    # Lógica para listar el catálogo de contenido
    print("Acción: Listar Catálogo de Contenido")

def ver_detalles_contenido():
    # Lógica para ver detalles de contenido
    print("Acción: Ver Detalles de Contenido")

def gestionar_pagos():
    # Lógica para gestionar pagos
    print("Acción: Gestionar Pagos")

def ver_estadisticas():
    # Lógica para ver estadísticas
    print("Acción: Ver Estadísticas")

if __name__ == '__main__':
    servidor_url = 'http://127.0.0.1:5000'

    while True:
        mostrar_menu()
        opcion = input("Ingresa el número de la acción que deseas realizar (0 para salir): ")

        if opcion == '0':
            break
        try:
            opcion = int(opcion)
        except ValueError:
            print("Ingresa un número válido.")
            continue

        if opcion == 1:
            cargar_archivo()
        elif opcion == 2:
            descargar_archivo()
        elif opcion == 3:
            ver_reportes()
        elif opcion == 4:
            gestionar_usuarios()
        elif opcion == 5:
            registrar_usuario()
        elif opcion == 6:
            iniciar_sesion()
        elif opcion == 7:
            listar_catalogo_contenido()
        elif opcion == 8:
            gestionar_pagos()
        elif opcion == 9:
            ver_estadisticas()
        else:
            print("Opción no válida. Ingresa un número del menú.")
            
    print("Saliendo del cliente.")
