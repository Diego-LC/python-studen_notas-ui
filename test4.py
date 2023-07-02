""" import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
import json
import os
from tkinter.filedialog import askdirectory

class VentanaNotas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Tabla de Notas")

        self.datos = [
            ("Control", 85, 0.4, "Evaluación Teórica", 0.6),
            ("Prueba", 92, 0.3, "Evaluación Práctica", 0.7),
            ("Tarea", 78, 0.2, "Evaluación Práctica", 0.8)
        ]

        self.frame_tabla = ttk.Frame(ventana)
        self.frame_tabla.pack(pady=20)

        self.tabla = ttk.Treeview(self.frame_tabla, columns=("Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"))
        self.tabla.pack(side=tk.LEFT)

        self.tabla.heading("#0", text="")
        self.tabla.heading("Tipo Nota", text="Tipo Nota")
        self.tabla.heading("Nota", text="Nota")
        self.tabla.heading("Ponderación Nota", text="Ponderación Nota")
        self.tabla.heading("Tipo Evaluación", text="Tipo Evaluación")
        self.tabla.heading("Ponderación Evaluación", text="Ponderación Evaluación")

        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Tipo Nota", anchor=tk.CENTER, width=100)
        self.tabla.column("Nota", anchor=tk.CENTER, width=100)
        self.tabla.column("Ponderación Nota", anchor=tk.CENTER, width=150)
        self.tabla.column("Tipo Evaluación", anchor=tk.CENTER, width=150)
        self.tabla.column("Ponderación Evaluación", anchor=tk.CENTER, width=200)

        self.tabla.bind("<Button-1>", self.editar_fila)

        self.frame_botones = ttk.Frame(ventana)
        self.frame_botones.pack(pady=10)

        btn_agregar = ttk.Button(self.frame_botones, text="Agregar Nota", command=self.agregar_nota)
        btn_agregar.grid(row=0, column=0, padx=5)

        btn_calcular_promedios = ttk.Button(self.frame_botones, text="Calcular Promedios", command=self.calcular_promedios)
        btn_calcular_promedios.grid(row=0, column=1, padx=5)

        btn_opciones = ttk.Button(self.frame_botones, text="Opciones", command=self.mostrar_opciones)
        btn_opciones.grid(row=0, column=2, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        for dato in self.datos:
            self.tabla.insert("", "end", text="", values=dato)

    def editar_fila(self, event):
        item_id = self.tabla.identify_row(event.y)
        fila_seleccionada = self.tabla.item(item_id)
        valores = fila_seleccionada['values']
        ventana_editar = tk.Toplevel(self.ventana)
        ventana_editar.title("Editar Nota")

        tipo_nota = tk.StringVar(value=valores[0])
        nota = tk.StringVar(value=valores[1])
        ponderacion_nota = tk.StringVar(value=valores[2])
        tipo_evaluacion = tk.StringVar(value=valores[3])
        ponderacion_evaluacion = tk.StringVar(value=valores[4])

        lbl_tipo_nota = tk.Label(ventana_editar, text="Tipo de Nota:")
        lbl_tipo_nota.pack()
        entry_tipo_nota = tk.Entry(ventana_editar, textvariable=tipo_nota)
        entry_tipo_nota.pack()

        lbl_nota = tk.Label(ventana_editar, text="Nota:")
        lbl_nota.pack()
        entry_nota = tk.Entry(ventana_editar, textvariable=nota)
        entry_nota.pack()

        lbl_ponderacion_nota = tk.Label(ventana_editar, text="Ponderación Nota:")
        lbl_ponderacion_nota.pack()
        entry_ponderacion_nota = tk.Entry(ventana_editar, textvariable=ponderacion_nota)
        entry_ponderacion_nota.pack()

        lbl_tipo_evaluacion = tk.Label(ventana_editar, text="Tipo de Evaluación:")
        lbl_tipo_evaluacion.pack()
        entry_tipo_evaluacion = tk.Entry(ventana_editar, textvariable=tipo_evaluacion)
        entry_tipo_evaluacion.pack()

        lbl_ponderacion_evaluacion = tk.Label(ventana_editar, text="Ponderación Evaluación:")
        lbl_ponderacion_evaluacion.pack()
        entry_ponderacion_evaluacion = tk.Entry(ventana_editar, textvariable=ponderacion_evaluacion)
        entry_ponderacion_evaluacion.pack()

        btn_guardar = tk.Button(ventana_editar, text="Guardar", command=lambda: self.guardar_edicion(item_id, tipo_nota.get(), nota.get(), ponderacion_nota.get(), tipo_evaluacion.get(), ponderacion_evaluacion.get(), ventana_editar))
        btn_guardar.pack()

        btn_eliminar = tk.Button(ventana_editar, text="Eliminar", command=lambda: self.eliminar_fila(item_id, ventana_editar))
        btn_eliminar.pack()

    def guardar_edicion(self, item_id, tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion, ventana_editar):
        self.tabla.item(item_id, text="", values=(tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion))
        ventana_editar.destroy()

    def eliminar_fila(self, item_id, ventana_editar):
        self.tabla.delete(item_id)
        ventana_editar.destroy()

    def agregar_nota(self):
        ventana_agregar = tk.Toplevel(self.ventana)
        ventana_agregar.title("Agregar Nota")

        tipo_nota = tk.StringVar()
        nota = tk.StringVar()
        ponderacion_nota = tk.StringVar()
        tipo_evaluacion = tk.StringVar()
        ponderacion_evaluacion = tk.StringVar()

        lbl_tipo_nota = tk.Label(ventana_agregar, text="Tipo de Nota:")
        lbl_tipo_nota.pack()
        entry_tipo_nota = tk.Entry(ventana_agregar, textvariable=tipo_nota)
        entry_tipo_nota.pack()

        lbl_nota = tk.Label(ventana_agregar, text="Nota:")
        lbl_nota.pack()
        entry_nota = tk.Entry(ventana_agregar, textvariable=nota)
        entry_nota.pack()

        lbl_ponderacion_nota = tk.Label(ventana_agregar, text="Ponderación Nota:")
        lbl_ponderacion_nota.pack()
        entry_ponderacion_nota = tk.Entry(ventana_agregar, textvariable=ponderacion_nota)
        entry_ponderacion_nota.pack()

        lbl_tipo_evaluacion = tk.Label(ventana_agregar, text="Tipo de Evaluación:")
        lbl_tipo_evaluacion.pack()
        entry_tipo_evaluacion = tk.Entry(ventana_agregar, textvariable=tipo_evaluacion)
        entry_tipo_evaluacion.pack()

        lbl_ponderacion_evaluacion = tk.Label(ventana_agregar, text="Ponderación Evaluación:")
        lbl_ponderacion_evaluacion.pack()
        entry_ponderacion_evaluacion = tk.Entry(ventana_agregar, textvariable=ponderacion_evaluacion)
        entry_ponderacion_evaluacion.pack()

        btn_agregar = tk.Button(ventana_agregar, text="Agregar", command=lambda: self.guardar_nota(tipo_nota.get(), nota.get(), ponderacion_nota.get(), tipo_evaluacion.get(), ponderacion_evaluacion.get(), ventana_agregar))
        btn_agregar.pack()

    def guardar_nota(self, tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion, ventana_agregar):
        self.tabla.insert("", "end", text="", values=(tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion))
        ventana_agregar.destroy()

    def calcular_promedios(self):
        df = pd.DataFrame(self.datos, columns=["Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"])
        promedios_evaluacion = df.groupby("Tipo Evaluación")["Nota"].mean()
        promedios_nota = df.groupby("Tipo Nota")["Nota"].mean()
        promedio_total = df["Nota"].mean()

        messagebox.showinfo("Promedios", f"Promedios por Tipo de Evaluación:\n\n{promedios_evaluacion}\n\nPromedios por Tipo de Nota:\n\n{promedios_nota}\n\nPromedio Total:\n\n{promedio_total}")

    def mostrar_opciones(self):
        ventana_opciones = tk.Toplevel(self.ventana)
        ventana_opciones.title("Opciones")

        btn_subir_servidor = tk.Button(ventana_opciones, text="Subir al Servidor", command=self.subir_servidor)
        btn_subir_servidor.pack(pady=10)

        btn_exportar_excel = tk.Button(ventana_opciones, text="Exportar a Excel", command=self.exportar_excel)
        btn_exportar_excel.pack(pady=10)

        btn_enviar_correo = tk.Button(ventana_opciones, text="Enviar por Correo", command=self.enviar_correo)
        btn_enviar_correo.pack(pady=10)

    def subir_servidor(self):
        datos_json = json.dumps(self.datos)
        # Lógica para enviar los datos al servidor

    def exportar_excel(self):
        df = pd.DataFrame(self.datos, columns=["Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"])
        directorio = askdirectory(title="Seleccione la carpeta de destino")
        if directorio:
            archivo = os.path.join(directorio, "datos.xlsx")
            df.to_excel(archivo, index=False)
            messagebox.showinfo("Exportar a Excel", "Los datos se han exportado exitosamente.")

    def enviar_correo(self):
        datos_json = json.dumps(self.datos)
        # Lógica para enviar los datos por correo

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = VentanaNotas(ventana_principal)
    ventana_principal.mainloop()
 """
import tkinter as tk
from tkinter import ttk

def on_selection(event):
    selected_item = combobox.get()
    print("Selected item:", selected_item)

# Crear la ventana
window = tk.Tk()
window.title("Combobox")
window.geometry("300x100")

# Variable para almacenar el valor seleccionado
selected_option = tk.StringVar()

# Crear el combobox con opciones y valor por defecto
combobox = ttk.Combobox(window, textvariable=selected_option)
combobox['values'] = ('Opción 1', 'Opción 2', 'Opción 3')
combobox.current(0)  # Establecer la opción por defecto (0-indexado)

# Asignar una función de callback para el evento de selección
combobox.bind('<<ComboboxSelected>>', on_selection)

# Mostrar el combobox
combobox.pack()

# Ejecutar el bucle principal
#window.mainloop()

datos = [{'ponderaciones':{'tipo_evaluacion':{'Eval. Práctica':0.4, 'Eval. Teórica':0.6}, 
                                            'tipo_nota':{'Prueba':0.6, 'Control':0.4, 'Trabajo':1.0}}},
                        {'notas':[["Control", "5.5", "Eval. Teórica"],
                                    ["Prueba", "6.0", "Eval. Teórica"],
                                    ["Control", "6.5", "Eval. Teórica"],
                                    ["Trabajo", "5.3", "Eval. Práctica"]]}]

nueva_lista = []

for nota in datos[1]['notas']:
    tipo_nota = nota[0]
    valor_nota = nota[1]
    tipo_evaluacion = nota[2]

    nueva_nota = [tipo_nota, valor_nota,
                  datos[0]['ponderaciones']['tipo_nota'][tipo_nota],
                  tipo_evaluacion,
                  datos[0]['ponderaciones']['tipo_evaluacion'][tipo_evaluacion]]
    
    nueva_lista.append(nueva_nota)

print(nueva_lista)
