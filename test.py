""" import random
import string

code_str = string.ascii_letters + string.digits
## Imprime 4 letras o números aleatorios
print(''.join(random.sample(code_str,6)))
p = 'asdfsdsd@gmail.com'
print('@' in p or '.c' in p) """

#ventana estudiante usando POO
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Asignatura:
    def __init__(self, titulo):
        self.titulo = titulo
        self.notas_practicas = []
        self.notas_teoricas = []

    def agregar_nota(self, tipo, ponderacion, valor):
        nota = {"tipo": tipo, "ponderacion": ponderacion, "valor": valor}
        if tipo == "Práctica":
            self.notas_practicas.append(nota)
        elif tipo == "Teórica":
            self.notas_teoricas.append(nota)

    def calcular_promedio_practicas(self):
        suma_ponderada = 0
        suma_ponderaciones = 0

        for nota in self.notas_practicas:
            suma_ponderada += nota["ponderacion"] * nota["valor"]
            suma_ponderaciones += nota["ponderacion"]

        if suma_ponderaciones > 0:
            return suma_ponderada / suma_ponderaciones
        else:
            return 0

    def calcular_promedio_teoricas(self):
        suma_ponderada = 0
        suma_ponderaciones = 0

        for nota in self.notas_teoricas:
            suma_ponderada += nota["ponderacion"] * nota["valor"]
            suma_ponderaciones += nota["ponderacion"]

        if suma_ponderaciones > 0:
            return suma_ponderada / suma_ponderaciones
        else:
            return 0

    def calcular_promedio_total(self):
        ponderacion_practicas = sum(nota["ponderacion"] for nota in self.notas_practicas)
        ponderacion_teoricas = sum(nota["ponderacion"] for nota in self.notas_teoricas)
        promedio_practicas = self.calcular_promedio_practicas()
        promedio_teoricas = self.calcular_promedio_teoricas()

        return (promedio_practicas * ponderacion_practicas + promedio_teoricas * ponderacion_teoricas) / (ponderacion_practicas + ponderacion_teoricas)

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.asignaturas = []
        self.title("Gestor de Asignaturas")
        
        self.frame_asignaturas = tk.Frame(self)
        self.frame_asignaturas.pack(pady=10)

        self.label_asignaturas = tk.Label(self.frame_asignaturas, text="Asignaturas:")
        self.label_asignaturas.pack()

        self.listbox_asignaturas = tk.Listbox(self.frame_asignaturas)
        self.listbox_asignaturas.pack()

        self.btn_agregar_asignatura = tk.Button(self, text="Agregar Asignatura", command=self.abrir_ventana_agregar_asignatura)
        self.btn_agregar_asignatura.pack(pady=5)

        self.btn_ver_asignatura = tk.Button(self, text="Ver Asignatura", command=self.ver_asignatura)
        self.btn_ver_asignatura.pack(pady=5)

    def abrir_ventana_agregar_asignatura(self):
        ventana_agregar_asignatura = VentanaAgregarAsignatura(self)
        # self.wait_window(ventana_agregar_asignatura)
        self.actualizar_listbox_asignaturas()

    def ver_asignatura(self):
        seleccion = self.listbox_asignaturas.curselection()
        if seleccion:
            index = seleccion[0]
            asignatura = self.asignaturas[index]
            ventana_ver_asignatura = VentanaVerAsignatura(self, asignatura)
            self.wait_window(ventana_ver_asignatura)

    def actualizar_listbox_asignaturas(self):
        self.listbox_asignaturas.delete(0, tk.END)
        for asignatura in self.asignaturas:
            self.listbox_asignaturas.insert(tk.END, asignatura.titulo)

class VentanaAgregarAsignatura(tk.Toplevel):
    def __init__(self, ventana_principal):
        super().__init__(ventana_principal)
        self.title("Agregar Asignatura")

        self.label_titulo = tk.Label(self, text="Título:")
        self.label_titulo.pack()

        self.entry_titulo = tk.Entry(self)
        self.entry_titulo.pack()

        self.btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_asignatura)
        self.btn_guardar.pack(pady=5)

    def guardar_asignatura(self):
        titulo = self.entry_titulo.get()
        if titulo:
            asignatura = Asignatura(titulo)
            self.master.asignaturas.append(asignatura)
            self.master.actualizar_listbox_asignaturas()
            self.destroy()
        else:
            messagebox.showerror("Error", "Debe ingresar un título.")

class VentanaVerAsignatura(tk.Toplevel):
    def __init__(self, ventana_principal, asignatura):
        super().__init__(ventana_principal)
        self.title(asignatura.titulo)

        self.label_notas_practicas = tk.Label(self, text="Notas Prácticas:")
        self.label_notas_practicas.pack()

        self.listbox_notas_practicas = tk.Listbox(self)
        self.listbox_notas_practicas.pack()

        self.frame_nota_practica = tk.Frame(self)
        self.frame_nota_practica.pack(pady=5)

        self.label_ponderacion_practica = tk.Label(self.frame_nota_practica, text="Ponderación Práctica:")
        self.label_ponderacion_practica.pack(side=tk.LEFT)

        self.entry_ponderacion_practica = tk.Entry(self.frame_nota_practica, width=5)
        self.entry_ponderacion_practica.pack(side=tk.LEFT)

        self.label_valor_practica = tk.Label(self.frame_nota_practica, text="Valor Práctica:")
        self.label_valor_practica.pack(side=tk.LEFT)

        self.entry_valor_practica = tk.Entry(self.frame_nota_practica, width=5)
        self.entry_valor_practica.pack(side=tk.LEFT)

        self.btn_agregar_nota_practica = tk.Button(self, text="Agregar Nota Práctica", command=self.agregar_nota_practica)
        self.btn_agregar_nota_practica.pack(pady=5)

        self.label_notas_teoricas = tk.Label(self, text="Notas Teóricas:")
        self.label_notas_teoricas.pack()

        self.listbox_notas_teoricas = tk.Listbox(self)
        self.listbox_notas_teoricas.pack()

        self.frame_nota_teorica = tk.Frame(self)
        self.frame_nota_teorica.pack(pady=5)

        self.label_ponderacion_teorica = tk.Label(self.frame_nota_teorica, text="Ponderación Teórica:")
        self.label_ponderacion_teorica.pack(side=tk.LEFT)

        self.entry_ponderacion_teorica = tk.Entry(self.frame_nota_teorica, width=5)
        self.entry_ponderacion_teorica.pack(side=tk.LEFT)

        self.label_valor_teorica = tk.Label(self.frame_nota_teorica, text="Valor Teórica:")
        self.label_valor_teorica.pack(side=tk.LEFT)

        self.entry_valor_teorica = tk.Entry(self.frame_nota_teorica, width=5)
        self.entry_valor_teorica.pack(side=tk.LEFT)

        self.btn_agregar_nota_teorica = tk.Button(self, text="Agregar Nota Teórica", command=self.agregar_nota_teorica)
        self.btn_agregar_nota_teorica.pack(pady=5)

        self.btn_calcular_promedio_practicas = tk.Button(self, text="Calcular Promedio Prácticas", command=self.calcular_promedio_practicas)
        self.btn_calcular_promedio_practicas.pack(pady=5)

        self.btn_calcular_promedio_teoricas = tk.Button(self, text="Calcular Promedio Teóricas", command=self.calcular_promedio_teoricas)
        self.btn_calcular_promedio_teoricas.pack(pady=5)

        self.btn_calcular_promedio_total = tk.Button(self, text="Calcular Promedio Total", command=self.calcular_promedio_total)
        self.btn_calcular_promedio_total.pack(pady=5)

        self.asignatura = asignatura

        self.actualizar_listbox_notas()

    def agregar_nota_practica(self):
        ponderacion = float(self.entry_ponderacion_practica.get())
        valor = float(self.entry_valor_practica.get())

        if ponderacion and valor:
            self.asignatura.agregar_nota("Práctica", ponderacion, valor)
            self.actualizar_listbox_notas()
            self.entry_ponderacion_practica.delete(0, tk.END)
            self.entry_valor_practica.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Debe ingresar todos los campos.")

    def agregar_nota_teorica(self):
        ponderacion = float(self.entry_ponderacion_teorica.get())
        valor = float(self.entry_valor_teorica.get())

        if ponderacion and valor:
            self.asignatura.agregar_nota("Teórica", ponderacion, valor)
            self.actualizar_listbox_notas()
            self.entry_ponderacion_teorica.delete(0, tk.END)
            self.entry_valor_teorica.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Debe ingresar todos los campos.")

    def calcular_promedio_practicas(self):
        promedio = self.asignatura.calcular_promedio_practicas()
        messagebox.showinfo("Promedio Prácticas", f"El promedio de las notas prácticas es: {promedio}")

    def calcular_promedio_teoricas(self):
        promedio = self.asignatura.calcular_promedio_teoricas()
        messagebox.showinfo("Promedio Teóricas", f"El promedio de las notas teóricas es: {promedio}")

    def calcular_promedio_total(self):
        promedio = self.asignatura.calcular_promedio_total()
        messagebox.showinfo("Promedio Total", f"El promedio total es: {promedio}")

    def actualizar_listbox_notas(self):
        self.listbox_notas_practicas.delete(0, tk.END)
        self.listbox_notas_teoricas.delete(0, tk.END)

        for nota in self.asignatura.notas_practicas:
            self.listbox_notas_practicas.insert(tk.END, f"Práctica - Ponderación: {nota['ponderacion']}, Valor: {nota['valor']}")

        for nota in self.asignatura.notas_teoricas:
            self.listbox_notas_teoricas.insert(tk.END, f"Teórica - Ponderación: {nota['ponderacion']}, Valor: {nota['valor']}")

ventana_principal = VentanaPrincipal()
ventana_principal.mainloop()
