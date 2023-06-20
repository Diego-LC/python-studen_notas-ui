import tkinter as tk

def open_main_window(vetana):
    # Cerrar la ventana de inicio de sesión
    vetana.destroy()
    
    # Crear la ventana principal
    main_window = tk.Tk()
    main_window.title("Ventana Principal")
    main_window.geometry("500x450")
    

    def logout():
    # Cerrar la ventana principal
        main_window.destroy()
    
    # Agregar contenido de la ventana principal
    
    btn_logout = tk.Button(main_window, text="Cerrar Sesión", command=logout)
    btn_logout.pack(pady=10)
    
    # Ejecutar la aplicación
    main_window.mainloop()
