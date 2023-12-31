import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.simpledialog import askstring
from openpyxl import Workbook
from openpyxl.styles import Alignment
from flask import jsonify
import requests
import datetime

class VentanaNotas:
    def __init__(self, ventana, datos):
        self.usuario = datos['userid']
        self.ventana = ventana
        self.ventana.title("Tabla de Notas")
        self.tipo_evaluacion = []
        self.seleccion = ""
        self.datos = datos['notas']
        self.api = "http://52.45.92.192:8081/"

        lbl_mensaje = tk.Label(ventana, text="Selecciona una fila para editarla", font=("Arial", 10), fg="blue")
        lbl_mensaje.grid(row=0, column=0, sticky="w", pady=(10, 0))

        self.frame_tabla = ttk.Frame(ventana)
        self.frame_tabla.grid(row=1, column=0, sticky="nswe")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=4)

        self.tabla = ttk.Treeview(self.frame_tabla, columns=("Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"))
        self.tabla.grid(row=1, column=0, sticky="nswe")
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
        btn_agregar.grid(row=4, column=0)

        btn_opciones = tk.Button(ventana, text="Opciones", command=self.mostrar_opciones)
        btn_opciones.grid(row=5, column=0, sticky="s")
        
        btn_cerrar_sesion = tk.Button(ventana, text="Cerrar Sesión", command=self.cerrar_sesion)
        btn_cerrar_sesion.grid(row=6, column=0, sticky="s", pady=(30,2))
    
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
            lbl_promedio_evaluaciones.grid(row=2, column=0, sticky="wn")
            lbl_promedio_total = tk.Label(self.ventana, text=f"Promedio Total: {self.promedio_total}")
            lbl_promedio_total.grid(row=3, column=0, sticky="ws")
    
    def calcular_promedios(self):
        promedios_tipo_evaluacion = {}
        #promedios_nota = {}
        promedio_total = 0.0
        
        for notas in self.datos[1]['notas']:
            tipo_nota = notas[0]
            ponderacion_nota = float(self.datos[0]['ponderaciones']['tipo_nota'][tipo_nota]) 
            tipo_eval = notas[2]
            if tipo_eval not in promedios_tipo_evaluacion.keys():
                promedios_tipo_evaluacion[tipo_eval] = (float(notas[1]) * ponderacion_nota)
                promedios_tipo_evaluacion[tipo_eval] = round(promedios_tipo_evaluacion[tipo_eval], 2)
            else:
                promedios_tipo_evaluacion[tipo_eval] += (float(notas[1]) * ponderacion_nota)
                promedios_tipo_evaluacion[tipo_eval] = round(promedios_tipo_evaluacion[tipo_eval], 2)
            """ if tipo_nota not in promedios_nota.keys():
                promedios_nota[tipo_nota] = (float(notas[1]) * ponderacion_nota)
            else:
                promedios_nota[tipo_nota] += (float(notas[1]) * ponderacion_nota) """
        
        for  ponderacion, promedio in promedios_tipo_evaluacion.items():
            ponderacion_evaluacion = float(self.datos[0]['ponderaciones']['tipo_evaluacion'][ponderacion])
            promedio_total += promedio * ponderacion_evaluacion

        return promedios_tipo_evaluacion, round(promedio_total, 2)

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
        self.seleccion = valores[3] # Valor por defecto del combobox
        def on_selection(event):
            self.seleccion = combobox.get() # Seleccionar el valor del combobox
        combobox = ttk.Combobox(ventana_editar, textvariable=tk.StringVar(), values=self.tipo_evaluacion)
        combobox.current(self.tipo_evaluacion.index(valores[3])) # Seleccionar el valor por defecto del combobox
        combobox.bind('<<ComboboxSelected>>', lambda event: on_selection(event)) # Evento para seleccionar un valor del combobox
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
        num_fila = self.tabla.index(item_id)
        if self.datos[1]['notas'][num_fila]:
            tipo_nota = self.datos[1]['notas'][num_fila][0]
            tipo_eval = self.datos[1]['notas'][num_fila][2]
            notnota = True
            noteval = True
            for fila in self.datos[1]['notas']:
                if tipo_nota in fila:
                    notnota = False
                if tipo_eval in fila:
                    noteval = False
            if notnota:
                del self.datos[0]['ponderaciones']['tipo_evaluacion'][tipo_eval]
            if noteval:
                del self.datos[0]['ponderaciones']['tipo_nota'][tipo_nota]
            del self.datos[1]['notas'][num_fila]
        self.cargar_datos()
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

    def mostrar_opciones(self):
        self.ventana.withdraw()
        ventana_opciones = tk.Toplevel(self.ventana)
        ventana_opciones.title("Opciones")
        ventana_opciones.geometry("180x230")
        ventana_opciones.resizable(False, False)

        btn_subir_servidor = tk.Button(ventana_opciones, text="Guardar cambios", command=self.subir_servidor)
        btn_subir_servidor.pack(pady=5)

        btn_exportar_excel = tk.Button(ventana_opciones, text="Exportar a Excel", command=self.exportar_excel)
        btn_exportar_excel.pack(pady=5)

        btn_enviar_correo = tk.Button(ventana_opciones, text="Enviar por Correo", command=self.enviar_correo)
        btn_enviar_correo.pack(pady=5)

        btn_volver = tk.Button(ventana_opciones, text="Volver", command=lambda: [self.ventana.deiconify(), ventana_opciones.destroy()])
        btn_volver.pack(pady=5, side=tk.BOTTOM)

    def subir_servidor(self):
        datos_json = {'userid': self.usuario, 'notas': self.datos}
        api_url = self.api + 'update'
        try:
            response = requests.post(api_url, json=datos_json)
            print(response)
        except:
            messagebox.showerror("Error", "Ha ocurrido un error al subir los datos al servidor.")
        if response.ok:
            respuesta = response.json()

            messagebox.showinfo("Subir al Servidor", respuesta['mensaje'])
        else:
            messagebox.showerror("Error", "Ha ocurrido un error al subir los datos al servidor.")

    def convertir_a_json(self):
        datos_json = {'userid': self.usuario, 'notas': {}}
        datos_json.update(self.datos[0])
        datos_json['promedios'] = self.promedio_evaluaciones
        datos_json['promedio_total'] = self.promedio_total
        index = 1
        if self.tabla.get_children():
            for item_id in self.tabla.get_children():
                datos_json['notas'][f'fila{index}'] = {'Tipo Nota': self.tabla.item(item_id)["values"][0], 
                                                        'Nota': self.tabla.item(item_id)["values"][1], 
                                                        'Ponderación Nota': self.tabla.item(item_id)["values"][2], 
                                                        'Tipo Evaluación': self.tabla.item(item_id)["values"][3]}
                index += 1
        print(datos_json)
        return datos_json

    def exportar_excel(self):
        libro_excel = Workbook()
        hoja = libro_excel.active
        datos = self.convertir_a_json()
        # Encabezados de las notas
        encabezados_notas = ['Tipo Nota', 'Nota', 'Ponderación Nota','Tipo Evaluación']
        hoja.append(encabezados_notas)

        # Escribir notas
        for fila_data in datos['notas'].values():
            fila = [fila_data['Tipo Nota'], fila_data['Nota'], fila_data['Ponderación Nota'],fila_data['Tipo Evaluación']]
            hoja.append(fila)

        # Espacio en blanco entre las notas y las ponderaciones
        hoja.append([])

        # Encabezados de las ponderaciones
        encabezados_ponderaciones = ['Tipo Evaluación', 'Ponderación']
        hoja.append(encabezados_ponderaciones)

        # Escribir ponderaciones
        for tipo_evaluacion, ponderacion in datos['ponderaciones']['tipo_evaluacion'].items():
            fila = [tipo_evaluacion, ponderacion]
            hoja.append(fila)

        # Espacio en blanco entre las ponderaciones y los promedios
        hoja.append([])
        hoja.append(['Promedios'])

        # Encabezados y valores de los promedios por tipo de evaluación
        encabezados_promedios = ['Tipo Evaluación', 'Promedio']
        hoja.append(encabezados_promedios)

        for tipo_evaluacion, promedio in datos['promedios'].items():
            fila = [tipo_evaluacion, promedio]
            hoja.append(fila)
        hoja.append([])

        # Encabezado y valor del promedio total
        encabezado_promedio_total = ['Promedio Total', datos['promedio_total']]
        hoja.append(encabezado_promedio_total)

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
        
        #Se pregunta por la ruta y nombre donde se guardará el archivo
        hoy = datetime.datetime.now()
        hoy_str = hoy.strftime("%d-%m-%Y_%H-%M-%S")
        ruta_archivo = asksaveasfilename(defaultextension=".xlsx", filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")), initialfile=f"Notas_{hoy_str}")
        
        if ruta_archivo:
            libro_excel.save(ruta_archivo)
            messagebox.showinfo("Exportar a Excel", f"Los datos se han exportado correctamente al archivo:\n\n{ruta_archivo}")

    def enviar_correo(self):
        datos_json =  self.convertir_a_json()
        api_url = self.api + 'send'
        try:
            response = requests.post(api_url, json=datos_json)
            print(response)
            messagebox.showinfo("Enviar por Correo", response.json()['mensaje'])
        except:
            messagebox.showinfo("Enviar por Correo", "Ha ocurrido un error al enviar los datos por correo")

    def cerrar_sesion(self):
        self.ventana.destroy()
        from inicio import root

def main_estudiante(ventana_login, datos):
    ventana_login.destroy()
    ventana_main = tk.Tk()
    ventana_main.resizable(width=False, height=False)
    app = VentanaNotas(ventana_main, datos)
    ventana_main.mainloop()