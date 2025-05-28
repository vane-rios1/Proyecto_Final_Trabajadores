import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Listas para almacenar los datos de trabajadores y asistencias
trabajadores = []
asistencias = []

# Función para limpiar el área dinámica antes de cargar una nueva pantalla
def limpiar_area():
    for widget in area_dinamica.winfo_children():
        widget.destroy()

# Pantalla de inicio
def pantalla_inicio():
    limpiar_area()
    tk.Label(area_dinamica, text="¡Bienvenido/a al Sistema del Hospital!", font=("Arial", 18, "bold")).pack(pady=20)
    tk.Label(area_dinamica, text="Este sistema permite registrar trabajadores y tomar asistencias.", font=("Arial", 12)).pack(pady=10)

# Pantalla para registrar trabajadores
def pantalla_registro_trabajador():
    limpiar_area()
    tk.Label(area_dinamica, text="Registro de Trabajador", font=("Arial", 14, "bold")).pack(pady=10)

    entradas = {}
    campos = [
        "Nombre", "Edad", "Género", "CURP", "No. de Seguro Social",
        "No. de Control", "Teléfono", "Domicilio"
    ]

    # Función auxiliar para crear una entrada de texto por cada campo
    def crear_entrada(campo):
        tk.Label(area_dinamica, text=f"{campo}:").pack()
        entrada = tk.Entry(area_dinamica)
        entrada.pack()
        entradas[campo] = entrada

    # Crear todas las entradas
    for campo in campos:
        crear_entrada(campo)

    # Guardar los datos del trabajador
    def guardar_trabajador():
        datos = {campo: entrada.get() for campo, entrada in entradas.items()}
        if not all(datos.values()):
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return
        trabajadores.append(datos)
        messagebox.showinfo("Guardado", "Trabajador registrado correctamente.")
        pantalla_registro_trabajador()  # Recargar la pantalla para limpiar los campos

    # Botón para guardar
    tk.Button(area_dinamica, text="Guardar Trabajador", command=guardar_trabajador).pack(pady=10)

# Pantalla para mostrar el historial de trabajadores registrados
def pantalla_historial_trabajadores():
    limpiar_area()
    tk.Label(area_dinamica, text="Historial de Trabajadores", font=("Arial", 14, "bold")).pack(pady=10)
    if trabajadores:
        for i, t in enumerate(trabajadores, 1):
            info = f"{i}. {t['Nombre']}, Edad: {t['Edad']}, Género: {t['Género']}, CURP: {t['CURP']}, No. de Control: {t['No. de Control']},  NSS: {t['No. de Seguro Social']}, Tel: {t['Teléfono']}, Domicilio: {t['Domicilio']}"
            tk.Label(area_dinamica, text=info, anchor="w", justify="left").pack()
    else:
        tk.Label(area_dinamica, text="No hay trabajadores registrados aún.").pack()

# Pantalla para registrar la asistencia de los trabajadores
def pantalla_registro_asistencia():
    limpiar_area()
    tk.Label(area_dinamica, text="Registro de Asistencia", font=("Arial", 14, "bold")).pack(pady=10)

    marco = tk.Frame(area_dinamica)
    marco.pack(pady=10)

    # Entradas para nombre, ID y departamento
    tk.Label(marco, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(marco)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(marco, text="ID:").grid(row=1, column=0, padx=5, pady=5)
    entry_id = tk.Entry(marco)
    entry_id.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(marco, text="Departamento:").grid(row=2, column=0, padx=5, pady=5)
    combo_departamento = ttk.Combobox(marco, values=["Enfermería", "Medicina", "Administración", "Limpieza", "Otro"])
    combo_departamento.grid(row=2, column=1, padx=5, pady=5)

    # Función para registrar la asistencia
    def registrar_asistencia():
        nombre = entry_nombre.get()
        empleado_id = entry_id.get()
        departamento = combo_departamento.get()
        if not nombre or not empleado_id or not departamento:
            messagebox.showwarning("Atención", "Por favor, completa todos los campos.")
            return
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = (nombre, empleado_id, departamento, fecha_hora)
        asistencias.append(registro)
        actualizar_tabla()  # Actualiza la tabla para mostrar el nuevo registro

        # Limpiar los campos
        entry_nombre.delete(0, tk.END)
        entry_id.delete(0, tk.END)
        combo_departamento.set("")

    # Botón para registrar la asistencia
    tk.Button(area_dinamica, text="Registrar Asistencia", command=registrar_asistencia).pack(pady=10)

    # Crear tabla para mostrar asistencias
    global tabla
    tabla = ttk.Treeview(area_dinamica, columns=("Nombre", "ID", "Departamento", "FechaHora"), show="headings")
    for col in ["Nombre", "ID", "Departamento", "FechaHora"]:
        tabla.heading(col, text=col)
    tabla.pack(padx=10, pady=10, fill="x")

    actualizar_tabla()

# Pantalla para ver el historial de asistencias
def pantalla_historial_asistencias():
    limpiar_area()
    tk.Label(area_dinamica, text="Historial de Asistencias", font=("Arial", 14, "bold")).pack(pady=10)

    tabla_local = ttk.Treeview(area_dinamica, columns=("Nombre", "ID", "Departamento", "FechaHora"), show="headings")
    for col in ["Nombre", "ID", "Departamento", "FechaHora"]:
        tabla_local.heading(col, text=col)
    tabla_local.pack(padx=10, pady=10, fill="x")

    # Mostrar los registros
    for registro in asistencias:
        tabla_local.insert("", "end", values=registro)

# Función para actualizar la tabla de asistencias en la pantalla de registro
def actualizar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for registro in asistencias:
        tabla.insert("", "end", values=registro)

# Confirmación antes de cerrar la aplicación
def confirmar_salida():
    if messagebox.askokcancel("Salir", "¿Deseas salir del sistema?"):
        ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión Hospitalaria")
ventana.geometry("800x600")
ventana.config(bg="lightblue")
ventana.protocol("WM_DELETE_WINDOW", confirmar_salida)

# Menú lateral
menu = tk.Frame(ventana, bg="lightblue", width=180)
menu.pack(side="left", fill="y")

# Área principal donde se muestran las diferentes pantallas
area_dinamica = tk.Frame(ventana, bg="white")
area_dinamica.pack(side="right", expand=True, fill="both")

# Botones del menú para navegar por las diferentes funciones del sistema
tk.Button(menu, text="Inicio", command=pantalla_inicio, width=20).pack(pady=5)
tk.Button(menu, text="Registrar Trabajador", command=pantalla_registro_trabajador, width=20).pack(pady=5)
tk.Button(menu, text="Ver Trabajadores", command=pantalla_historial_trabajadores, width=20).pack(pady=5)
tk.Button(menu, text="Registrar Asistencia", command=pantalla_registro_asistencia, width=20).pack(pady=5)
tk.Button(menu, text="Ver Asistencias", command=pantalla_historial_asistencias, width=20).pack(pady=5)
tk.Button(menu, text="Salir", command=confirmar_salida, width=20).pack(pady=20)

# Mostrar pantalla de inicio al iniciar el programa
pantalla_inicio()

# Iniciar el bucle principal de la interfaz
ventana.mainloop()

       
      
       
