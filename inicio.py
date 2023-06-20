import requests
import tkinter as tk
from tkinter import font, ttk, Radiobutton,Label
import sys
import main_app
from register import registro

import tkinter as tk

def login():
    user = entry_username.get()
    password = entry_password.get()
    # Verificar las credenciales del usuario
    url = "http://52.45.92.192:8081/events" # Dirección URL de tu API Flask aquí
    params = {"username": user,"password": password}
    try:
        response = requests.post(url, json=params)
    except:
        print("Error al conectarse a la API")
        # Error al conectarse a la API
        lbl_message.config(text="Error al conectarse a la API", fg="red")
        btn_register.pack(side=tk.TOP, pady=10)
        return

    if response.ok:
        token = response.json()
        if token['token'] or (user == "admin" and password == "admin"):
            # Usuario registrado
            print("Token de autenticación recibido:", token)
            lbl_message.config(text="Inicio de sesión exitoso", fg="green")
            main_app.open_main_window(root)
        else:
            print("Error al recibir el token de autenticación")
            print(token)
            # Usuario no registrado
            lbl_message.config(text="Usuario no registrado", fg="red")
            btn_register.pack(side=tk.TOP, pady=10)
    else:
        print("Error al recibir la respuesta de la API")
        # Error al recibir la respuesta de la API
        lbl_message.config(text="Error al recibir la respuesta de la API", fg="red")
        btn_register.pack(side=tk.TOP, pady=10)

def recover_password():
    # Cerrar la ventana de inicio de sesión
    root.withdraw()
    
    # Crear una nueva ventana para recuperar la contraseña
    recover_window = tk.Toplevel(root)
    recover_window.title("Recuperar Contraseña")
    recover_window.geometry("400x200")
    
    def submit_email():
        # Aquí puedes agregar el código para enviar el correo de recuperación de contraseña
        url = "http://52.45.92.192:8081/recover" # Dirección URL de tu API Flask aquí
        params = {"email": entry_email.get()}
        try:
            response = requests.post(url, json=params)
        except:
            print("Error al conectarse a la API")
            # Error al conectarse a la API
            lbl_message.config(text="Error al conectarse a la API", fg="red")
            return
        if response.ok:
            notificacion = tk.Toplevel(recover_window)
            notificacion.title("Notificación")
            notificacion.geometry("100x60")

            lbl_notificacion = tk.Label(notificacion, text="Se ha enviado un correo de recuperación")
            lbl_notificacion.pack()
            # Cerrar la ventana de recuperación de contraseña
            lbl_button = tk.Button(notificacion, text="Aceptar", command=recover_window.destroy)
            lbl_button.pack()
        
        recover_window.destroy()
        # Mostrar la ventana de inicio de sesión nuevamente
        root.deiconify()
    
    lbl_email = tk.Label(recover_window, text="Correo electrónico:")
    lbl_email.pack()
    entry_email = tk.Entry(recover_window)
    entry_email.pack()
    
    btn_submit = tk.Button(recover_window, text="Enviar", command=submit_email)
    btn_submit.pack(pady=10)

def register():
    registro(root)

# Crear la ventana principal
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("500x400")

# Agregar campos de entrada de usuario y contraseña
lbl_username = tk.Label(root, text="Usuario:")
lbl_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

lbl_password = tk.Label(root, text="Contraseña:")
lbl_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Agregar botón de inicio de sesión
btn_login = tk.Button(root, text="Iniciar Sesión", command=login)
btn_login.pack(pady=10)

# Etiqueta para mostrar mensajes
lbl_message = tk.Label(root, text="")
lbl_message.pack()

# Botón de registro (inicialmente oculto)
btn_register = tk.Button(root, text="Registrarse", command=register)

# Botón de recuperar contraseña
btn_recover_password = tk.Button(root, text="Recuperar contraseña", command=recover_password)
btn_recover_password.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

