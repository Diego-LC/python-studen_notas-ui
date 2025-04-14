import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook
from openpyxl.styles import Alignment
from tkinter.filedialog import asksaveasfilename
import requests
import datetime

class BarraMenu(tk.Menu):
    def __init__(self, ventana_principal, datos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana_principal = ventana_principal
        self.ventana_asignatura = Ventana_asignaturas(self.ventana_principal, datos)
        self.idusuario = datos['userid']
        self.asignaturas = datos['asignaturas']
        self.barra_menu = tk.Menu()
        self.menu_opciones = tk.Menu(self.barra_menu, tearoff=0)
        self.menu_opciones.add_command(label="Agregar Asignatura", accelerator="Ctrl+N", command=self.ventana_asignatura.ventana_agregar_asignatura)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Guardar en servidor", accelerator="Ctrl+S", command=self.subir_servidor)
        self.menu_opciones.add_command(label="Exportar a excel", accelerator="Ctrl+G", command=self.exportar_excel)
        self.menu_opciones.add_command(label="Enviar por Correo", accelerator="Ctrl+E", command=self.enviar_correo)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        self.barra_menu.add_cascade(label="Opciones", menu=self.menu_opciones)

        # Asociar el atajo del teclado del menú "Nuevo".
        ventana_principal.bind_all("<Control-n>", self.ventana_asignatura.ventana_agregar_asignatura)
        ventana_principal.bind_all("<Control-s>", self.subir_servidor)
        ventana_principal.bind_all("<Control-g>", self.exportar_excel)
        ventana_principal.bind_all("<Control-e>", self.enviar_correo)
        ventana_principal.bind_all("<Control-x>", self.archivo_open_presionado)
        self.ventana_principal.config(menu=self.barra_menu)

    def convertir_lista(self):
        datos = {'userid': self.idusuario, 'asignaturas': {}}
        for asignatura in self.asignaturas.keys():
            header = [
                ['DATOS ASIGNATURA'],
                ['Asignatura', self.asignaturas[asignatura]['codigo']+' '+ asignatura],
                ['N° Módulo:', self.asignaturas[asignatura]['modulo']],
                ['Año:',self.asignaturas[asignatura]['año'], 'Semestre:', self.asignaturas[asignatura]['semestre']],
                [],['']
                ]
            datos['asignaturas'][asignatura] = [header]
            for tipo_eval, val in self.asignaturas[asignatura]['ponderaciones']['tipo_evaluacion'].items():
                header[4].extend([f'% {tipo_eval}:', f'{int(val)*100}%',''])
                notas = [[tipo_eval+':'],
                        ['N°','Tipo eval.','Descripción','Fecha Eval.','Nota','Ponderación']
                        ]
                index = 1
                for nota in self.asignaturas[asignatura]['notas']:
                    if nota[2] == tipo_eval:
                        fila = [str(index), nota[0], self.asignaturas[asignatura]['descripcion'], 
                                self.asignaturas[asignatura]['fecha'], nota[1], 
                                f"{float(self.asignaturas[asignatura]['ponderaciones']['tipo_nota'][nota[0]])*100}%"]
                        notas.append(fila)
                        index += 1
                datos['asignaturas'][asignatura].append(notas)
                datos['asignaturas'][asignatura].append([['']])
        return datos

    def exportar_excel(self,*args):
        def ajustar_celdas(hoja):
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
        
        libro_excel = Workbook()
        hoja = libro_excel.active
        hoja.title = "Asignaturas"
        datos = self.convertir_lista()
        # Encabezados de las asignaturas
        encabezados_asignaturas = ['Código', 'Módulo', 'Asignatura']
        hoja.append(encabezados_asignaturas)

        # Escribir filas de asignaturas
        for asignatura in datos['asignaturas'].keys():
            hoja.append([self.asignaturas[asignatura]['codigo'], self.asignaturas[asignatura]['modulo'], asignatura])

        ajustar_celdas(hoja)

        # Crear hojas de asignaturas y escribir datos
        for asignatura, datos in datos['asignaturas'].items():
            nueva_hoja = libro_excel.create_sheet(asignatura)
            nueva_hoja.title = asignatura
            for tabla in datos:
                for fila in tabla:
                    nueva_hoja.append(fila)
            ajustar_celdas(nueva_hoja)

        #Se pregunta por la ruta y nombre donde se guardará el archivo
        hoy = datetime.datetime.now()
        hoy_str = hoy.strftime("%d-%m-%Y_%H-%M-%S")
        ruta_archivo = asksaveasfilename(defaultextension=".xlsx", filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")), initialfile=f"Notas_{hoy_str}")
        
        if ruta_archivo:
            libro_excel.save(ruta_archivo)
            messagebox.showinfo("Exportar a Excel", f"Los datos se han exportado correctamente al archivo:\n\n{ruta_archivo}")

    def archivo_open_presionado(self,*args):
        print("¡Has presionado para abrir archivo!")

    def subir_servidor(self,*args):
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

    def enviar_correo(self,*args):
        datos_json =  self.convertir_lista()
        api_url = self.api + 'send'
        try:
            response = requests.post(api_url, json=datos_json)
            print(response)
            messagebox.showinfo("Enviar por Correo", response.json()['mensaje'])
        except:
            messagebox.showinfo("Enviar por Correo", "Ha ocurrido un error al enviar los datos por correo")

    def cerrar_sesion(self,*args):
        self.ventana_principal.destroy()
        from inicio_sesion import ventana_inicio
        ventana_inicio()


class Ventana_asignaturas:
    def __init__(self, ventana, datos):
        self.asignaturas = datos['asignaturas']
        self.usuario = datos['userid']
        self.ventana_principal = ventana
        self.barra_menu = None
        self.ventana_principal.title("Asignaturas")
        self.ventana_principal.geometry("300x450")
        self.ventana_principal.resizable(width=False, height=False)
        self.ventana_principal.focus()

        self.label_lista = tk.Label(self.ventana_principal, text="Lista de asignaturas:")
        self.label_lista.pack(pady=(20,5))

        self.listbox_asignaturas = tk.Listbox(self.ventana_principal)
        self.listbox_asignaturas.pack()

        self.btn_ver_asignatura = tk.Button(self.ventana_principal, text="Ver Asignatura", command=self.ver_asignatura)
        self.btn_renombrar_asignatura = tk.Button(self.ventana_principal, text="Renombrar Asignatura", command=self.renombrar_asignatura)

        self.listbox_asignaturas.bind("<<ListboxSelect>>", self.seleccionar_asignatura)
        self.ventana_principal.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.ventana_principal.bind("<ButtonRelease-3>", self.abrir_menu_click_derecho)
        
        ventana.bind_all("<Control-n>", self.ventana_agregar_asignatura)
        self.actualizar_listbox_asignaturas()

        
    def abrir_menu_click_derecho(self, event):
        click_listbox = self.on_listbox_click(event)
        self.ventana_click_derecho(click_listbox)
        try:
            if click_listbox:
            # Si se hace click derecho sobre un elemento de la lista, se selecciona ese elemento y se muestra el menú
                self.listbox_asignaturas.select_clear(0, tk.END)
                self.listbox_asignaturas.selection_set(self.listbox_asignaturas.nearest(event.y))
        finally:
            self.menu_click_derecho.tk_popup(event.x_root, event.y_root)
            self.menu_click_derecho.grab_release()
    
    def ventana_click_derecho(self, click_listbox):
        m = tk.Menu(self.ventana_principal, tearoff = 0)
        
        if click_listbox:
            m.add_command(label ="Abrir", command=self.ver_asignatura)
            m.add_command(label ="Renombrar", command=self.renombrar_asignatura)
            m.add_command(label ="Eliminar", command=self.eliminar_asignatura)
            m.add_command(label ="Recargar", command=self.actualizar_listbox_asignaturas)
            m.add_separator()
        m.add_command(label ="Salir", command=self.ventana_principal.destroy)
        self.menu_click_derecho = m

    def on_listbox_click(self, event):
        # Obtener las coordenadas del clic
        x, y = event.x, event.y
        
        # Si las coordenadas están dentro del Listbox
        if 0 <= x < self.listbox_asignaturas.winfo_width() and 0 <= y < self.listbox_asignaturas.winfo_height():
            click = True
        else:
            #Clic fuera del Listbox
            self.listbox_asignaturas.selection_clear(0, tk.END)  # Limpiar la selección
            click = False
        return click
    
    def seleccionar_asignatura(self, event):
        titulo = self.listbox_asignaturas.get(self.listbox_asignaturas.curselection())
        if titulo:
            self.btn_ver_asignatura.pack(pady=5) # Mostrar el botón 'ver asignatura'
            self.btn_renombrar_asignatura.pack(pady=5) # Mostrar el botón 'renombrar asignatura'
        return titulo

    def actualizar_listbox_asignaturas(self):
        self.listbox_asignaturas.delete(0, tk.END)
        for asignatura in self.asignaturas.keys():
            self.listbox_asignaturas.insert(tk.END, asignatura)

    def ventana_agregar_asignatura(self, *args):
        self.ventana_agregar = tk.Toplevel(self.ventana_principal)
        self.ventana_agregar.title("Agregar Asignatura")
        self.ventana_agregar.geometry("260x250")
        self.ventana_agregar.focus()
        self.ventana_agregar.grab_set()

        label_titulo = tk.Label(self.ventana_agregar, text="Nombre asignatura:")
        label_titulo.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.entry_titulo = tk.Entry(self.ventana_agregar)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        label_codigo = tk.Label(self.ventana_agregar, text="Código:")
        label_codigo.grid(row=1, column=0, pady=5)
        self.entry_codigo = tk.Entry(self.ventana_agregar)
        self.entry_codigo.grid(row=1, column=1, pady=5)
        label_modulo = tk.Label(self.ventana_agregar, text="Módulo:")
        label_modulo.grid(row=2, column=0, pady=5)
        self.entry_modulo = tk.Entry(self.ventana_agregar)
        self.entry_modulo.grid(row=2, column=1, pady=5)

        label_año = tk.Label(self.ventana_agregar, text="Año:")
        label_año.grid(row=3, column=0, pady=5)
        self.entry_año = tk.Entry(self.ventana_agregar)
        self.entry_año.grid(row=3, column=1, pady=5)
        label_semestre = tk.Label(self.ventana_agregar, text="Semestre:")
        label_semestre.grid(row=4, column=0, pady=5)
        self.entry_semestre = tk.Entry(self.ventana_agregar)
        self.entry_semestre.grid(row=4, column=1, pady=5)

        btn_agregar = tk.Button(self.ventana_agregar, text="Agregar", command=self.agregar_asignatura)
        btn_agregar.grid(row=5, column=0, columnspan=3,sticky='S', pady=(20,5))
    
    def agregar_asignatura(self):
        titulo = self.entry_titulo.get()
        self.entry_titulo.delete(0, tk.END)
        codigo = self.entry_codigo.get()
        modulo = self.entry_modulo.get()
        año = self.entry_año.get()
        semestre = self.entry_semestre.get()
        if titulo:
            asignatura = {titulo: 
                                {'ponderaciones':
                                            {'tipo_evaluacion':{'Eval. Teórica':1.0}, 
                                            'tipo_nota':{'Control':0.4, 'Prueba': 0.6}
                                            },
                                'notas':[
                                        ["Control", "5.5", "Eval. Teórica"],
                                        ["Prueba", "5.2", "Eval. Teórica"]
                                        ],
                                'codigo': codigo or '',
                                'modulo': modulo or '',
                                'año': año or '',
                                'semestre': semestre or '',
                                'fecha':'',
                                'descripcion':''}
                        }
            self.asignaturas.update(asignatura)
            self.actualizar_listbox_asignaturas()
            self.ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Debe ingresar una asignatura.")

    def ver_asignatura(self):
        indice = self.listbox_asignaturas.curselection()
        if indice:
            asignatura = self.listbox_asignaturas.get(indice[0])
            from ventana_asignatura import abrir_ventana_notas
            abrir_ventana_notas(self.ventana_principal, self.asignaturas[asignatura], asignatura)

    def renombrar_asignatura(self):
        indice = self.listbox_asignaturas.curselection()
        if indice:
            asignatura = self.listbox_asignaturas.get(indice[0])
            self.ventana_renombrar_asignatura(asignatura)
        
    def ventana_renombrar_asignatura(self, asignatura):
        ventana = tk.Toplevel()
        ventana.transient(self.ventana_principal)
        ventana.title("Renombrar asignatura")
        ventana.focus()
        ventana.grab_set()

        label_titulo = tk.Label(ventana, text="Nuevo nombre:")
        label_titulo.pack()

        entry_titulo = tk.Entry(ventana)
        entry_titulo.insert(0, asignatura)
        entry_titulo.pack()

        btn_renombrar = tk.Button(ventana, text="Renombrar", command=lambda: self.renombrar(entry_titulo, ventana, asignatura))
        btn_renombrar.pack(pady=5)
        ventana.wait_window()

    def renombrar(self, entrada, ventana, asignatura):
        titulo = entrada.get()
        if titulo:
            self.asignaturas[titulo] = self.asignaturas.pop(asignatura)
            ventana.destroy()
            self.actualizar_listbox_asignaturas()
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre.")

    def eliminar_asignatura(self):
        indice = self.listbox_asignaturas.curselection()
        if indice:
            asignatura = self.listbox_asignaturas.get(indice[0])
            self.asignaturas.pop(asignatura)
            self.actualizar_listbox_asignaturas()

def main_ventana(ventana_login, datos):
    ventana_login.destroy()
    ventana_main = tk.Tk()
    a = BarraMenu(ventana_main, datos)
    ventana_main.mainloop()

datos = {'userid':1,'asignaturas':{
                            'Algebra lineal':{
                                            'ponderaciones':
                                                    {'tipo_evaluacion':{'Eval. Teórica':1.0}, 
                                                    'tipo_nota':{'Control':0.4, 'Prueba': 0.6}
                                                    },
                                            'notas':[
                                                    ["Control", "5.5", "Eval. Teórica"],
                                                    ["Prueba", "5.2", "Eval. Teórica"]
                                                    ],
                                            'codigo':'',
                                            'modulo':'',
                                            'año':'',
                                            'semestre':'',
                                            'fecha':'',
                                            'descripcion':''
                                            },
                            'Programación': {
                                                'ponderaciones':
                                                        {'tipo_evaluacion':{'Eval. Teórica':1.0}, 
                                                        'tipo_nota':{'Control':0.4, 'Prueba': 0.6}}
                                                    ,
                                                    
                                                'notas':[
                                                        ["Control", "5.5", "Eval. Teórica"],
                                                        ["Prueba", "5.2", "Eval. Teórica"]
                                                        ],
                                                'codigo':'',
                                                'modulo':'',
                                                'año':'',
                                                'semestre':'',
                                                'fecha':'',
                                                'descripcion':''
                                    }}}

#{'tabl' : [
#   [
#       ['DATOS ASIGNATURA'], 
#       ['Asignatura:', 'IME299 ÁLGEBRA LINEAL'], 
#       ['Nº Módulo:', '4'], 
#       ['Año:', '2023', 'Semestre:', '1'], 
#       ['Académico(s)', ''], 
#       ['% Teórico', '100', '% Práctico', '0']
#   ], 
#   [
#       ['Teórica'], 
#       ['Nº', 'Tipo Eval.', 'Descripción', 'Fecha Eval.', 'Nota', 'Ponderación', 'Doc.'], 
#       ['1', 'Control', 'Control 1', '13/04/2023', '5.8', '15.00%', ''], 
#       ['2', 'Prueba', 'Primera Prueba parcial', '27/04/2023', '6.1', '35.00%', ''], 
#       ['3', 'Control', 'Control 2', '15/06/2023', '4.4', '15.00%', ''], 
#       ['4', 'Prueba', 'Segunda prueba parcial', '29/06/2023', '4.6', '35.00%', '']
#   ]
# ]}
root = tk.Tk()
main_ventana(root, datos)
