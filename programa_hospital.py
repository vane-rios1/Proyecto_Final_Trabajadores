import tkinter as tk
from tkinter import messagebox

# Parte del Programa "Registro de Trabajadores del Hospital"

# Lista para almacenar trabajadores
trabajadores = []

def limpiar_area_dinamica():
    for widget in area_dinamica.winfo_children():
        widget.destroy()

def pantalla_inicio():
    limpiar_area_dinamica()
    tk.Label(area_dinamica, text="¡Bienvenido/a!", font=("Arial", 18, "bold")).pack(pady=20)
    tk.Label(area_dinamica, text="Hola, esta aplicación lleva el control del registro los trabajadores de este hospital .", font=("Arial", 12)).pack(pady=10)

def pantalla_registro():
    limpiar_area_dinamica()
    tk.Label(area_dinamica, text="Datos del trabajador", font=("Arial", 14, "bold")).pack(pady=10)

    entradas = {}

    def crear_entrada(campo):
        tk.Label(area_dinamica, text=f"{campo}:").pack()
        entrada = tk.Entry(area_dinamica)
        entrada.pack()
        entradas[campo] = entrada

    campos = [
        "Nombre", "Edad", "Género", "CURP", "No. de Seguro Social",
        "No. de Control", "Teléfono", "Domicilio"
    ]
    
    for campo in campos:
        crear_entrada(campo)

    def guardar_datos():
        datos = {campo: entrada.get() for campo, entrada in entradas.items()}

        if not all(datos.values()):
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return

        trabajadores.append(datos)
        messagebox.showinfo("Guardado", "Datos del trabajador guardados correctamente.")
        pantalla_registro()  # Limpia el formulario

    tk.Button(area_dinamica, text="Guardar datos", command=guardar_datos).pack(pady=10)

def pantalla_historial():
    limpiar_area_dinamica()
    tk.Label(area_dinamica, text="Historial de Trabajadores", font=("Arial", 14, "bold")).pack(pady=10)

    if trabajadores:
        for i, t in enumerate(trabajadores, 1):
            info = f"{i}. {t['Nombre']} - Edad: {t['Edad']} - Género: {t['Género']} - CURP: {t['CURP']} - NSS: {t['No. de Seguro Social']} - Numero de control: {t['No. de Control']} - Teléfono: {t['Teléfono']}  - Domicilio: {t['Domicilio']}"
            tk.Label(area_dinamica, text=info, anchor="w", justify="left").pack()
    else:
        tk.Label(area_dinamica, text="No hay trabajadores registrados aún.").pack()

# Ventana principal
ventana = tk.Tk()
ventana.title("Registro de Trabajadores")
ventana.geometry("600x500")
ventana.config(bg="lightblue")

menu = tk.Frame(ventana, bg="lightblue", width=150)
menu.pack(side="left", fill="y")

area_dinamica = tk.Frame(ventana, bg="white")
area_dinamica.pack(side="right", expand=True, fill="both")

# Menú de navegación
tk.Button(menu, text="Bienvenida", command=pantalla_inicio, width=18).pack(pady=5)
tk.Button(menu, text="Registrar", command=pantalla_registro, width=18).pack(pady=5)
tk.Button(menu, text="Trabajadores", command=pantalla_historial, width=18).pack(pady=20)
tk.Button(menu, text="Salir", command=ventana.destroy, width=18).pack(pady=30)

pantalla_inicio()
ventana.mainloop()
