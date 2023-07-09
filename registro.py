import tkinter as tk
import requests

api = "http://52.45.92.192:8081/"
def registro(root):
    # Cerrar la ventana de inicio de sesión
    root.withdraw()
    
    # Crear una nueva ventana para el formulario de registro
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("500x450")
    
    def send_verification_code():
        # Aquí puedes agregar el código para enviar el código de validación al correo electrónico
        email = entry_email.get()
        url = api+"email_verification"
        params = {"email": email}
        try:
            response = requests.post(url, json=params)
        except:
            print("Error al conectarse a la API")
            # Error al conectarse a la API
            lbl_verification_code.config(text="Error al conectarse a la API", fg="red")
            lbl_verification_code.pack()
            return
        if response.ok:
            mensaje = response.json()['mensaje']
            if response.json()['status']:
                print("Código de validación enviado")
                lbl_verification_code.config(text=mensaje, fg="green")
                lbl_verification_code.pack()
                entry_verification_code.pack()
                btn_submit.pack(pady=10)
                # Mostrar el campo de código de validación
            else:
                print("Email ya se encuentra registrado")
                # Error al enviar el código de validación
                lbl_verification_code.config(text=mensaje, fg="red")
                lbl_verification_code.pack()
        else:
            print("Error al enviar el código de validación")
            # Error al enviar el código de validación
            lbl_verification_code.config(text="Error al enviar el código de validación", fg="red")
            lbl_verification_code.pack()
    
    def submit_form():
        # Aquí puedes agregar el código para enviar el formulario
        nombre = entry_name.get()
        matricula = entry_matricula.get()
        usuario = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()
        codigo = entry_verification_code.get()
        url = api+"register"
        params = {"name": nombre, "matricula": matricula, "username": usuario, "password": password, "email": email, "code": codigo}
        try:
            response = requests.post(url, json=params)
        except:
            print("Error al conectarse a la API")
            # Error al conectarse a la API
            lbl_message = tk.Label(register_window, text="Error al conectarse a la API", fg="red")
            lbl_message.pack()
            return
        if response.ok:
            respuesta = response.json()
            if respuesta['status']:
                print("Registro exitoso")
                # Registro exitoso
                lbl_message = tk.Label(register_window, text=respuesta['mensaje'], fg="green")
                lbl_message.pack()
                register_window.destroy()
                root.deiconify()
            else:
                print("Error codigo de validacion incorrecto")
                # Error al registrar
                lbl_message = tk.Label(register_window, text=respuesta['mensaje'], fg="red")
                lbl_message.pack()
        # Cerrar la ventana de registro
        
        # Mostrar la ventana de inicio de sesión nuevamente
    
    lbl_title = tk.Label(register_window, text="Registro")
    lbl_title.pack(pady=10)
    lbl_name = tk.Label(register_window, text="Nombres:")
    lbl_name.pack()
    entry_name = tk.Entry(register_window)
    entry_name.pack()

    lbl_matricula = tk.Label(register_window, text="Matrícula:")
    lbl_matricula.pack()
    entry_matricula = tk.Entry(register_window)
    entry_matricula.pack()
    
    lbl_username = tk.Label(register_window, text="Usuario:")
    lbl_username.pack()
    entry_username = tk.Entry(register_window)
    entry_username.pack()
    
    lbl_password = tk.Label(register_window, text="Contraseña:")
    lbl_password.pack()
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack()
    
    lbl_email = tk.Label(register_window, text="Correo electrónico:")
    lbl_email.pack()
    entry_email = tk.Entry(register_window)
    entry_email.pack()
    
    btn_send_verification_code = tk.Button(register_window, text="Enviar Código de Validación", command=send_verification_code)
    btn_send_verification_code.pack(pady=10)
    
    lbl_verification_code = tk.Label(register_window, text="Código de validación:")
    entry_verification_code = tk.Entry(register_window)
    
    btn_submit = tk.Button(register_window, text="Enviar", command=submit_form)

    btn_volver = tk.Button(register_window, text="Volver", command=lambda: [register_window.destroy(), root.deiconify()])
    btn_volver.pack(pady=(50,0), side=tk.BOTTOM)
