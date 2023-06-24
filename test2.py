import tkinter as tk
from tkinter import messagebox
#Ventana estudiante enfoque estructurado
asignaturas = []

def agregar_asignatura():
    titulo = entry_titulo.get()
    if titulo:
        asignatura = {"titulo": titulo, "notas_practicas": [], "notas_teoricas": []}
        asignaturas.append(asignatura)
        actualizar_listbox_asignaturas()
    else:
        messagebox.showerror("Error", "Debe ingresar un título.")

def ver_asignatura():
    seleccion = listbox_asignaturas.curselection()
    if seleccion:
        index = seleccion[0]
        asignatura = asignaturas[index]
        ventana_ver_asignatura(asignatura)

def ventana_ver_asignatura(asignatura):
    ventana = tk.Toplevel()
    ventana.title(asignatura["titulo"])

    def agregar_nota(tipo):
        ponderacion = float(entry_ponderacion.get())
        valor = float(entry_valor.get())

        if ponderacion and valor:
            nota = {"ponderacion": ponderacion, "valor": valor}
            if tipo == "Práctica":
                asignatura["notas_practicas"].append(nota)
            elif tipo == "Teórica":
                asignatura["notas_teoricas"].append(nota)
            actualizar_listbox_notas()
            entry_ponderacion.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Debe ingresar todos los campos.")

    def calcular_promedio(tipo):
        notas = asignatura["notas_practicas"] if tipo == "Práctica" else asignatura["notas_teoricas"]
        if notas:
            suma_ponderada = sum(nota["ponderacion"] * nota["valor"] for nota in notas)
            suma_ponderaciones = sum(nota["ponderacion"] for nota in notas)
            promedio = suma_ponderada / suma_ponderaciones
            messagebox.showinfo(f"Promedio {tipo}s", f"El promedio de las notas {tipo}s es: {promedio}")
        else:
            messagebox.showinfo(f"Promedio {tipo}s", "No hay notas registradas.")

    label_notas_practicas = tk.Label(ventana, text="Notas Prácticas:")
    label_notas_practicas.pack()

    listbox_notas_practicas = tk.Listbox(ventana)
    listbox_notas_practicas.pack()

    frame_nota_practica = tk.Frame(ventana)
    frame_nota_practica.pack(pady=5)

    label_ponderacion_practica = tk.Label(frame_nota_practica, text="Ponderación Práctica:")
    label_ponderacion_practica.pack(side=tk.LEFT)

    entry_ponderacion_practica = tk.Entry(frame_nota_practica, width=5)
    entry_ponderacion_practica.pack(side=tk.LEFT)

    label_valor_practica = tk.Label(frame_nota_practica, text="Valor Práctica:")
    label_valor_practica.pack(side=tk.LEFT)

    entry_valor_practica = tk.Entry(frame_nota_practica, width=5)
    entry_valor_practica.pack(side=tk.LEFT)

    btn_agregar_nota_practica = tk.Button(ventana, text="Agregar Nota Práctica", command=lambda: agregar_nota("Práctica"))
    btn_agregar_nota_practica.pack(pady=5)

    label_notas_teoricas = tk.Label(ventana, text="Notas Teóricas:")
    label_notas_teoricas.pack()

    listbox_notas_teoricas = tk.Listbox(ventana)
    listbox_notas_teoricas.pack()

    frame_nota_teorica = tk.Frame(ventana)
    frame_nota_teorica.pack(pady=5)

    label_ponderacion_teorica = tk.Label(frame_nota_teorica, text="Ponderación Teórica:")
    label_ponderacion_teorica.pack(side=tk.LEFT)

    entry_ponderacion_teorica = tk.Entry(frame_nota_teorica, width=5)
    entry_ponderacion_teorica.pack(side=tk.LEFT)

    label_valor_teorica = tk.Label(frame_nota_teorica, text="Valor Teórica:")
    label_valor_teorica.pack(side=tk.LEFT)

    entry_valor_teorica = tk.Entry(frame_nota_teorica, width=5)
    entry_valor_teorica.pack(side=tk.LEFT)

    btn_agregar_nota_teorica = tk.Button(ventana, text="Agregar Nota Teórica", command=lambda: agregar_nota("Teórica"))
    btn_agregar_nota_teorica.pack(pady=5)

    btn_calcular_promedio_practicas = tk.Button(ventana, text="Calcular Promedio Prácticas", command=lambda: calcular_promedio("Práctica"))
    btn_calcular_promedio_practicas.pack(pady=5)

    btn_calcular_promedio_teoricas = tk.Button(ventana, text="Calcular Promedio Teóricas", command=lambda: calcular_promedio("Teórica"))
    btn_calcular_promedio_teoricas.pack(pady=5)

    btn_calcular_promedio_total = tk.Button(ventana, text="Calcular Promedio Total", command=lambda: calcular_promedio("Total"))
    btn_calcular_promedio_total.pack(pady=5)

    def actualizar_listbox_notas():
        listbox_notas_practicas.delete(0, tk.END)
        listbox_notas_teoricas.delete(0, tk.END)

        for nota in asignatura["notas_practicas"]:
            listbox_notas_practicas.insert(tk.END, f"Práctica - Ponderación: {nota['ponderacion']}, Valor: {nota['valor']}")

        for nota in asignatura["notas_teoricas"]:
            listbox_notas_teoricas.insert(tk.END, f"Teórica - Ponderación: {nota['ponderacion']}, Valor: {nota['valor']}")

ventana_principal = tk.Tk()

label_titulo = tk.Label(ventana_principal, text="Título:")
label_titulo.pack()

entry_titulo = tk.Entry(ventana_principal)
entry_titulo.pack()

btn_agregar = tk.Button(ventana_principal, text="Agregar", command=agregar_asignatura)
btn_agregar.pack(pady=5)

listbox_asignaturas = tk.Listbox(ventana_principal)
listbox_asignaturas.pack()

btn_ver_asignatura = tk.Button(ventana_principal, text="Ver Asignatura", command=ver_asignatura)
btn_ver_asignatura.pack(pady=5)

def actualizar_listbox_asignaturas():
    listbox_asignaturas.delete(0, tk.END)
    for asignatura in asignaturas:
        listbox_asignaturas.insert(tk.END, asignatura["titulo"])

ventana_principal.mainloop()
