import requests
import tkinter as tk
from tkinter import font, ttk, Radiobutton,Label
import sys
import main_app

""" 

## main
root = tk.Tk()
root.config(width=500, height=400)

entry = ttk.Entry(font=font.Font(family="Times", size=18))
etiqueta = Label(root, text="Ingrese rut:")
etiqueta.place(x=20, y=50)
etiqueta.config(font=font.Font(family="Times", size=18))
entry.place(x=50, y=50)
entry.insert(1, "")

entry.place(x=180, y=50)
button = ttk.Button(text="Obtener texto", command=lambda: boton_presionado())
button.place(x=50, y=100)
"""

import tkinter as tk

def login():
    user = entry_username.get()
    password = entry_password.get()
    # Verificar las credenciales del usuario
    url = "http://52.45.92.192:8081/events" # Dirección URL de tu API Flask aquí
    params = {"username": user,"password": password}
    response = requests.post(url, json=params)

    if response.ok:
        token = response.json()
        if token['token'] == 'True' or (user == "admin" and password == "admin"):
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

def register():
    # Cerrar la ventana de inicio de sesión
    root.withdraw()
    
    # Crear una nueva ventana para el formulario de registro
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("500x450")
    
    def send_verification_code():
        # Aquí puedes agregar el código para enviar el código de validación al correo electrónico
        
        # Mostrar el campo de código de validación
        lbl_verification_code.pack()
        entry_verification_code.pack()
        btn_submit.pack(pady=10)
    
    def submit_form():
        # Aquí puedes agregar el código para enviar el formulario
        
        # Cerrar la ventana de registro
        register_window.destroy()
        
        # Mostrar la ventana de inicio de sesión nuevamente
        root.deiconify()
    
    lbl_name = tk.Label(register_window, text="Nombre:")
    lbl_name.pack()
    entry_name = tk.Entry(register_window)
    entry_name.pack()
    
    lbl_username = tk.Label(register_window, text="Usuario:")
    lbl_username.pack()
    entry_username = tk.Entry(register_window)
    entry_username.pack()
    
    lbl_email = tk.Label(register_window, text="Correo electrónico:")
    lbl_email.pack()
    entry_email = tk.Entry(register_window)
    entry_email.pack()
    
    lbl_password = tk.Label(register_window, text="Contraseña:")
    lbl_password.pack()
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack()
    
    btn_send_verification_code = tk.Button(register_window, text="Enviar Código de Validación", command=send_verification_code)
    btn_send_verification_code.pack(pady=10)
    
    lbl_verification_code = tk.Label(register_window, text="Código de validación:")
    entry_verification_code = tk.Entry(register_window, show="*")
    
    btn_submit = tk.Button(register_window, text="Enviar", command=submit_form)

def recover_password():
    # Cerrar la ventana de inicio de sesión
    root.withdraw()
    
    # Crear una nueva ventana para recuperar la contraseña
    recover_window = tk.Toplevel(root)
    recover_window.title("Recuperar Contraseña")
    recover_window.geometry("400x200")
    
    def submit_email():
        # Aquí puedes agregar el código para enviar el correo de recuperación de contraseña
        
        # Cerrar la ventana de recuperación de contraseña
        recover_window.destroy()
        
        # Mostrar la ventana de inicio de sesión nuevamente
        root.deiconify()
    
    lbl_email = tk.Label(recover_window, text="Correo electrónico:")
    lbl_email.pack()
    entry_email = tk.Entry(recover_window)
    entry_email.pack()
    
    btn_submit = tk.Button(recover_window, text="Enviar", command=submit_email)
    btn_submit.pack(pady=10)

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

