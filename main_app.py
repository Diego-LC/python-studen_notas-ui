import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.simpledialog import askstring
from openpyxl import Workbook
from openpyxl.styles import Alignment
from flask import jsonify

class VentanaNotas:
    def __init__(self, ventana, datos):
        self.ventana = ventana
        self.ventana.title("Tabla de Notas")
        self.tipo_evaluacion = []
        self.seleccion = ""
        self.datos = datos

        self.frame_tabla = ttk.Frame(ventana)
        self.frame_tabla.grid(row=0, column=0, sticky="nswe")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=4)

        self.tabla = ttk.Treeview(self.frame_tabla, columns=("Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"))
        self.tabla.pack(side=tk.LEFT)
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Tipo Nota", anchor=tk.CENTER, width=100)
        self.tabla.column("Nota", anchor=tk.CENTER, width=100)
        self.tabla.column("Ponderación Nota", anchor=tk.CENTER, width=140)
        self.tabla.column("Tipo Evaluación", anchor=tk.CENTER, width=120)
        self.tabla.column("Ponderación Evaluación", anchor=tk.CENTER, width=180)

        self.tabla.heading("#0", text="")
        self.tabla.heading("Tipo Nota", text="Tipo de Nota")
        self.tabla.heading("Nota", text="Nota")
        self.tabla.heading("Ponderación Nota", text="Ponderación Nota")
        self.tabla.heading("Tipo Evaluación", text="Tipo de Evaluación")
        self.tabla.heading("Ponderación Evaluación", text="Ponderación Evaluación")
        self.tabla.bind("<Button-1>", self.editar_fila) # Evento para editar una fila
        
        self.cargar_datos() # Cargar los datos de la tabla
        
        btn_agregar = tk.Button(ventana, text="Agregar Nota", command=self.agregar_nota)
        btn_agregar.grid(row=3, column=0)

        btn_opciones = tk.Button(ventana, text="Opciones", command=self.mostrar_opciones)
        btn_opciones.grid(row=4, column=0, sticky="s")
    
    def cargar_datos(self):
        nueva_lista = []
        # limpiar los datos de la tabla
        self.tabla.delete(*self.tabla.get_children())
        if len(self.datos) != 0:
            for tipo_evaluacion in self.datos[0]['ponderaciones']['tipo_evaluacion'].keys():
                self.tipo_evaluacion.append(tipo_evaluacion)
            for nota in self.datos[1]['notas']:
                tipo_nota = nota[0]
                tipo_evaluacion = nota[2]
                valor_nota = nota[1]
                nueva_nota = [tipo_nota, valor_nota,
                            self.datos[0]['ponderaciones']['tipo_nota'][tipo_nota],
                            tipo_evaluacion,
                            self.datos[0]['ponderaciones']['tipo_evaluacion'][tipo_evaluacion]]
                nueva_lista.append(nueva_nota)

            for dato in nueva_lista:
                self.tabla.insert("", "end", text="", values=dato)
            self.tabla.grid(row=0, column=0, sticky="nswe")

            self.promedio_evaluaciones, self.promedio_total = self.calcular_promedios()
            mensaje = ''
            for evaluacion, promedio in self.promedio_evaluaciones.items():
                mensaje += f"{evaluacion}: {promedio}\n"
            lbl_promedio_evaluaciones = tk.Label(self.ventana, text=mensaje)
            lbl_promedio_evaluaciones.grid(row=1, column=0, sticky="wn")
            lbl_promedio_total = tk.Label(self.ventana, text=f"Promedio Total: {self.promedio_total}")
            lbl_promedio_total.grid(row=2, column=0, sticky="ws")
            print(self.promedio_evaluaciones)
            #lbl_promedio_evaluaciones.update()

    
    def editar_fila(self, event):
        item_id = self.tabla.identify_row(event.y)
        num_fila = self.tabla.index(item_id)
        fila_seleccionada = self.tabla.item(item_id)
        valores = fila_seleccionada['values']
        ventana_editar = tk.Toplevel(self.ventana)
        ventana_editar.title("Editar Nota")

        tipo_nota = tk.StringVar(value=valores[0])
        nota = tk.StringVar(value=valores[1])
        ponderacion_nota = tk.StringVar(value=valores[2])
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
        self.seleccion = valores[3]
        print("Sin seleccionar", self.seleccion)
        def on_selection(event):
            self.seleccion = combobox.get()
            print("Seleccionado item:", self.seleccion)
        combobox = ttk.Combobox(ventana_editar, textvariable=tk.StringVar(), values=self.tipo_evaluacion)
        combobox.current(self.tipo_evaluacion.index(valores[3]))
        combobox.bind('<<ComboboxSelected>>', lambda event: on_selection(event))
        combobox.pack(pady=5)

        lbl_ponderacion_evaluacion = tk.Label(ventana_editar, text="Ponderación Evaluación:")
        lbl_ponderacion_evaluacion.pack()
        entry_ponderacion_evaluacion = tk.Entry(ventana_editar, textvariable=ponderacion_evaluacion)
        entry_ponderacion_evaluacion.pack()

        btn_guardar = tk.Button(ventana_editar, text="Guardar", command=lambda: 
                                self.guardar_edicion( tipo_nota.get(), nota.get(),ponderacion_nota.get(), combobox.get(), 
                                                    ponderacion_evaluacion.get(), ventana_editar, num_fila))
        btn_guardar.pack()

        btn_eliminar = tk.Button(ventana_editar, text="Eliminar", command=lambda: self.eliminar_fila(item_id, ventana_editar))
        btn_eliminar.pack()

    def guardar_edicion(self, tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion, ventana_editar, num_fila):
        if tipo_evaluacion not in self.datos[0]['ponderaciones']:
            del self.datos[0]['ponderaciones']['tipo_evaluacion'][self.seleccion]
            self.datos[0]['ponderaciones']['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
        for datos in self.datos[1].values():
            if datos[num_fila]:
                datos[num_fila][0] = tipo_nota
                datos[num_fila][1] = nota
                datos[num_fila][2] = tipo_evaluacion
            for dato in datos:
                if dato[2] == self.seleccion:
                    print("De ", dato[2], "a ", tipo_evaluacion)
                    dato[2] = tipo_evaluacion

        for dato in self.datos[0].values():
                dato['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
                dato['tipo_nota'][tipo_nota] = ponderacion_nota
        self.cargar_datos()
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

        lbl_ponderacion_evaluacion = tk.Label(ventana_agregar, text="Ponderación según tipo de evaluación:")
        lbl_ponderacion_evaluacion.pack()
        entry_ponderacion_evaluacion = tk.Entry(ventana_agregar, textvariable=ponderacion_evaluacion)
        entry_ponderacion_evaluacion.pack()

        btn_agregar = tk.Button(ventana_agregar, text="Agregar", command=lambda: self.guardar_nota(tipo_nota.get(), nota.get(), ponderacion_nota.get(), tipo_evaluacion.get(), ponderacion_evaluacion.get(), ventana_agregar))
        btn_agregar.pack()

    def guardar_nota(self, tipo_nota, nota, ponderacion_nota, tipo_evaluacion, ponderacion_evaluacion, ventana_agregar):
        self.datos[1]['notas'].append([tipo_nota, nota, tipo_evaluacion])
        self.datos[0]['ponderaciones']['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
        self.datos[0]['ponderaciones']['tipo_nota'][tipo_nota] = ponderacion_nota
        self.cargar_datos()
        ventana_agregar.destroy()

    def calcular_promedios(self):
        promedios_tipo_evaluacion = {}
        #promedios_nota = {}
        promedio_total = 0.0
        
        for notas in self.datos[1]['notas']:
            tipo_nota = notas[0]
            ponderacion_nota = float(self.datos[0]['ponderaciones']['tipo_nota'][tipo_nota]) 
            tipo_eval = notas[2]
            if tipo_eval not in promedios_tipo_evaluacion.keys():
                promedios_tipo_evaluacion[tipo_eval] = round(float(notas[1]) * ponderacion_nota, 2)
            else:
                promedios_tipo_evaluacion[tipo_eval] += round(float(notas[1]) * ponderacion_nota, 2)
            """ if tipo_nota not in promedios_nota.keys():
                promedios_nota[tipo_nota] = (float(notas[1]) * ponderacion_nota)
            else:
                promedios_nota[tipo_nota] += (float(notas[1]) * ponderacion_nota) """
        
        for  ponderacion, promedio in promedios_tipo_evaluacion.items():
            ponderacion_evaluacion = float(self.datos[0]['ponderaciones']['tipo_evaluacion'][ponderacion])
            promedio_total += promedio * ponderacion_evaluacion

        return promedios_tipo_evaluacion, round(promedio_total, 2)
        messagebox.showinfo("Promedios", f"Promedios por Tipo de Evaluación:\n\n{promedios_tipo_evaluacion}\n\nPromedios por Tipo de Nota:\n\n{promedios_nota}\n\nPromedio Total: {promedio_total:.2f}")

    def mostrar_opciones(self):
        ventana_opciones = tk.Toplevel(self.ventana)
        ventana_opciones.title("Opciones")

        btn_subir_servidor = tk.Button(ventana_opciones, text="Guardar cambios", command=self.subir_servidor)
        btn_subir_servidor.pack(pady=5)

        btn_exportar_excel = tk.Button(ventana_opciones, text="Exportar a Excel", command=self.exportar_excel)
        btn_exportar_excel.pack(pady=5)

        btn_enviar_correo = tk.Button(ventana_opciones, text="Enviar por Correo", command=self.enviar_correo)
        btn_enviar_correo.pack(pady=5)

    def subir_servidor(self):
        datos_json = self.convertir_a_json()
        print(datos_json)
        # Aquí puedes implementar la lógica para subir los datos al servidor
        messagebox.showinfo("Subir al Servidor", "Los datos se han subido correctamente al servidor.")

    def convertir_a_json(self):
        datos_json = {}
        index = 1
        for fila in self.datos:
            datos_json['fila' + str(index)] ={
                "Tipo Nota": fila[0],
                "Nota": fila[1],
                "Ponderación Nota": fila[2],
                "Tipo Evaluación": fila[3],
                "Ponderación Evaluación": fila[4]
            }
            index += 1
        return datos_json

    def exportar_excel(self):
        nombre_archivo = askstring("Guardar como", "Ingrese el nombre del archivo Excel:")
        if nombre_archivo:
            ruta_archivo = asksaveasfilename(defaultextension=".xlsx", filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")))
            if ruta_archivo:
                libro_excel = Workbook()
                hoja = libro_excel.active

                # Encabezados de columna
                hoja.append(["Tipo de Nota", "Nota", "Ponderación Nota", "Tipo de Evaluación", "Ponderación Evaluación"])

                # Datos de la tabla
                for fila in self.datos:
                    hoja.append(fila)

                # Ajustar el ancho de las columnas
                for columna in hoja.columns:
                    max_length = 0
                    column = columna[0].column_letter  # Obtiene la letra de la columna (A, B, C, ...)
                    for cell in columna:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    hoja.column_dimensions[column].width = adjusted_width

                # Centrar el contenido de las celdas
                for fila in hoja.iter_rows(min_row=2):
                    for celda in fila:
                        celda.alignment = Alignment(horizontal="center", vertical="center")

                libro_excel.save(ruta_archivo)
                messagebox.showinfo("Exportar a Excel", f"Los datos se han exportado correctamente al archivo:\n\n{ruta_archivo}")

    def enviar_correo(self):
        datos_json = self.convertir_a_json()
        print(datos_json)
        # Aquí puedes implementar la lógica para enviar los datos por correo utilizando el formato JSON
        messagebox.showinfo("Enviar por Correo", "Los datos se han enviado correctamente por correo.")

def main_estudiante(ventana, datos):
    ventana.destroy()
    ventana_main = tk.Tk()
    ventana_main.resizable(width=False, height=False)
    app = VentanaNotas(ventana_main, datos)
    ventana_main.mainloop()