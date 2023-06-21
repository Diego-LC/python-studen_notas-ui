import tkinter as tk

def main_profesor(vetana):
    # Cerrar la ventana de inicio de sesión
    vetana.destroy()
    
    # Crear la ventana principal
    window_profesor = tk.Tk()
    window_profesor.title("Ventana profesor")
    window_profesor.geometry("500x450")
    

    def logout():
    # Cerrar la ventana principal
        window_profesor.destroy()
    
    # Agregar contenido de la ventana principal
    
    btn_logout = tk.Button(window_profesor, text="Cerrar Sesión", command=logout)
    btn_logout.pack(pady=10)
    
    # Ejecutar la aplicación
    window_profesor.mainloop()

def main_estudiante(ventana):
    ventana.destroy()
    window_estudiante = tk.Tk()
    window_estudiante.title("Ventana estudiante")
    window_estudiante.geometry("500x450")

    window_estudiante.mainloop()