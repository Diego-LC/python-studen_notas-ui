import tkinter as tk

def registro(root):
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
    entry_verification_code = tk.Entry(register_window, show="*")
    
    btn_submit = tk.Button(register_window, text="Enviar", command=submit_form)
