import requests
import tkinter as tk
import main_app
from registro import registro

api = "http://52.45.92.192:8081/"
def login():
    user = entry_username.get()
    password = entry_password.get()
    # Verificar las credenciales del usuario
    url = api + "login" # Dirección URL de tu API Flask aquí
    params = {"username": user,"password": password}
    datos_admin={'userid': 1, 'notas': [{'ponderaciones':{'tipo_nota':{'Prueba':0.6, 'Control':0.4, 'Tarea':1.0},
                                                        'tipo_evaluacion':{'Eval. Teórica':0.7 , 'Eval. Práctica':0.3}}},
                                        {'notas':[["Control", "5.5", "Eval. Teórica"],
                                                    ["Prueba", "6.0", "Eval. Teórica"],
                                                    ['Tarea', '6.0', 'Eval. Práctica']]}]}
    try:
        response = requests.post(url, json=params)
    except:
        print("Error al conectarse a la API")
        # Error al conectarse a la API
        lbl_message.config(text="Error al conectarse a la API", fg="red")
        if user == "admin" or password == "admin":
            main_app.main_estudiante(root, datos_admin)
        return

    if response.ok:
        respuesta = response.json()
        if respuesta['token']:
            # Usuario registrado
            print("Token de autenticación recibido:", respuesta['token'])
            main_app.main_estudiante(root, respuesta)
        else:
            print("Error al iniciar sesión")
            print(respuesta)
            # Usuario no registrado
            lbl_message.config(text=respuesta['mensaje'], fg="red")
    else:
        print("Error al recibir la respuesta de la API")
        lbl_message.config(text="Error al recibir la respuesta de la API", fg="red")
    if user == "admin" or password == "admin":
        main_app.main_estudiante(root, datos_admin)

def recover_password():
    # Cerrar la ventana de inicio de sesión
    root.withdraw()
    
    # Crear una nueva ventana para recuperar la contraseña
    recover_window = tk.Toplevel(root)
    recover_window.title("Recuperar Contraseña")
    recover_window.geometry("400x200")
    
    def submit_email():
        # Aquí puedes agregar el código para enviar el correo de recuperación de contraseña
        url = api + "recover" # Dirección URL de tu API Flask aquí
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

            lbl_notificacion = tk.Label(notificacion, text=response.json()['mensaje'])
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

    btn_volver = tk.Button(recover_window, text="Volver", command=lambda: (recover_window.destroy(), root.deiconify()))
    btn_volver.pack(pady=(50,0))

# Crear la ventana principal
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("500x400")

# Agregar campos de entrada de usuario y contraseña
lbl_username = tk.Label(root, text="Usuario o email:")
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
btn_register = tk.Button(root, text="Registrarse", command=lambda: registro(root))
btn_register.pack(side=tk.TOP, pady=10)

# Botón de recuperar contraseña
btn_recover_password = tk.Button(root, text="Recuperar contraseña", command=recover_password)
btn_recover_password.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
