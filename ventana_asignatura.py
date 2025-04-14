import tkinter as tk
from tkinter import ttk, messagebox
from flask import jsonify

class VentanaNotas:
    def __init__(self, ventana, datos):
        self.ventana = ventana
        self.ventana.title("Tabla de Notas")
        self.tipo_evaluacion = []
        self.seleccion = ""
        self.datos = datos
        self.api = "http://52.45.92.192:8081/"

        lbl_mensaje = tk.Label(ventana, text="Selecciona una fila para editarla", font=("Arial", 10), fg="blue")
        lbl_mensaje.grid(row=0, column=0, sticky="w", pady=(10, 0))

        self.frame_tabla = ttk.Frame(ventana)
        self.frame_tabla.grid(row=1, column=0, sticky="nswe")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=4)

#        self.frame_tabla2 = ttk.Frame(ventana)
#        self.frame_tabla2.grid(row=2, column=0, sticky="nswe")
#        self.frame_tabla2.columnconfigure(0, weight=1)
#        self.frame_tabla2.rowconfigure(0, weight=4)

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

        self.tabla2 = ttk.Treeview(self.frame_tabla, columns=("Tipo Nota", "Nota", "Ponderación Nota", "Tipo Evaluación", "Ponderación Evaluación"))
        self.tabla2.grid(row=2, column=0, sticky="nswe")
        self.tabla2.column("#0", width=0, stretch=tk.NO)
        self.tabla2.column("Tipo Nota", anchor=tk.CENTER, width=100)
        self.tabla2.column("Nota", anchor=tk.CENTER, width=100)
        self.tabla2.column("Ponderación Nota", anchor=tk.CENTER, width=140)
        self.tabla2.column("Tipo Evaluación", anchor=tk.CENTER, width=120)
        self.tabla2.column("Ponderación Evaluación", anchor=tk.CENTER, width=180)

        self.tabla2.heading("#0", text="")
        self.tabla2.heading("Tipo Nota", text="Tipo de Nota")
        self.tabla2.heading("Nota", text="Nota")
        self.tabla2.heading("Ponderación Nota", text="Ponderación Nota")
        self.tabla2.heading("Tipo Evaluación", text="Tipo de Evaluación")
        self.tabla2.heading("Ponderación Evaluación", text="Ponderación Evaluación")
        
        self.cargar_datos() # Cargar los datos de la tabla
        
        btn_agregar = tk.Button(ventana, text="Agregar Nota", command=self.agregar_nota)
        btn_agregar.grid(row=4, column=0, pady=(10, 5))

        btn_volver = tk.Button(ventana, text="Volver", command=ventana.destroy)
        btn_volver.grid(row=5, column=0, pady=(5, 5))
    
    def cargar_datos(self):
        nueva_lista = []
        # limpiar los datos de la tabla
        self.tabla.delete(*self.tabla.get_children()) 
        if len(self.datos) != 0:
            for tipo_evaluacion in self.datos['ponderaciones']['tipo_evaluacion'].keys():
                self.tipo_evaluacion.append(tipo_evaluacion)
            for nota in self.datos['notas']:
                tipo_nota = nota[0]
                tipo_evaluacion = nota[2]
                valor_nota = nota[1]
                nueva_nota = [tipo_nota, valor_nota,
                            self.datos['ponderaciones']['tipo_nota'][tipo_nota],
                            tipo_evaluacion,
                            self.datos['ponderaciones']['tipo_evaluacion'][tipo_evaluacion]]
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
        
        for notas in self.datos['notas']:
            tipo_nota = notas[0]
            ponderacion_nota = float(self.datos['ponderaciones']['tipo_nota'][tipo_nota]) 
            tipo_eval = notas[2]
            if tipo_eval not in promedios_tipo_evaluacion.keys():
                promedios_tipo_evaluacion[tipo_eval] = (float(notas[1]) * ponderacion_nota)
                promedios_tipo_evaluacion[tipo_eval] = round(promedios_tipo_evaluacion[tipo_eval], 2)
            else:
                promedios_tipo_evaluacion[tipo_eval] += (float(notas[1]) * ponderacion_nota)
                promedios_tipo_evaluacion[tipo_eval] = round(promedios_tipo_evaluacion[tipo_eval], 2)
        
        for  ponderacion, promedio in promedios_tipo_evaluacion.items():
            ponderacion_evaluacion = float(self.datos['ponderaciones']['tipo_evaluacion'][ponderacion])
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
        if tipo_evaluacion not in self.datos['ponderaciones']:
            del self.datos['ponderaciones']['tipo_evaluacion'][self.seleccion]
            self.datos['ponderaciones']['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
        for datos in self.datos.values():
            if datos[num_fila]:
                datos[num_fila][0] = tipo_nota
                datos[num_fila][1] = nota
                datos[num_fila][2] = tipo_evaluacion
            for dato in datos:
                if dato[2] == self.seleccion:
                    print("De ", dato[2], "a ", tipo_evaluacion)
                    dato[2] = tipo_evaluacion

        for dato in self.datos.values():
                dato['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
                dato['tipo_nota'][tipo_nota] = ponderacion_nota
        self.cargar_datos()
        ventana_editar.destroy()

    def eliminar_fila(self, item_id, ventana_editar):
        num_fila = self.tabla.index(item_id)
        if self.datos['notas'][num_fila]:
            tipo_nota = self.datos['notas'][num_fila][0]
            tipo_eval = self.datos[1]['notas'][num_fila][2]
            notnota = True
            noteval = True
            for fila in self.datos['notas']:
                if tipo_nota in fila:
                    notnota = False
                if tipo_eval in fila:
                    noteval = False
            if notnota:
                del self.datos['ponderaciones']['tipo_evaluacion'][tipo_eval]
            if noteval:
                del self.datos['ponderaciones']['tipo_nota'][tipo_nota]
            del self.datos['notas'][num_fila]
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
        self.datos['notas'].append([tipo_nota, nota, tipo_evaluacion])
        self.datos['ponderaciones']['tipo_evaluacion'][tipo_evaluacion] = ponderacion_evaluacion
        self.datos['ponderaciones']['tipo_nota'][tipo_nota] = ponderacion_nota
        self.cargar_datos()
        ventana_agregar.destroy()

def abrir_ventana_notas(ventana_padre, datos, asignatura):
    #ventana_login.destroy()
    ventana_main = tk.Toplevel()
    ventana_main.resizable(width=False, height=False)
    ventana_main.transient(ventana_padre)
    ventana_main.title(asignatura)
    ventana_main.focus()
    ventana_main.grab_set()
    app = VentanaNotas(ventana_main, datos)
    ventana_main.mainloop()