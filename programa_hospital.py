import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Clase principal del sistema hospitalario
class SistemaHospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Hospitalaria")
        self.root.geometry("800x600")
        self.root.config(bg="lightblue")
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

        # Datos almacenados
        self.trabajadores = []
        self.asistencias = []

        # Estructura de la interfaz
        self.menu = tk.Frame(self.root, bg="lightblue", width=180)
        self.menu.pack(side="left", fill="y")

        self.area_dinamica = tk.Frame(self.root, bg="white")
        self.area_dinamica.pack(side="right", expand=True, fill="both")

        self.tabla = None  # Tabla de asistencias

        # Botones del menú
        tk.Button(self.menu, text="Inicio", command=self.pantalla_inicio, width=20).pack(pady=5)
        tk.Button(self.menu, text="Registrar Trabajador", command=self.pantalla_registro_trabajador, width=20).pack(pady=5)
        tk.Button(self.menu, text="Ver Trabajadores", command=self.pantalla_historial_trabajadores, width=20).pack(pady=5)
        tk.Button(self.menu, text="Registrar Asistencia", command=self.pantalla_registro_asistencia, width=20).pack(pady=5)
        tk.Button(self.menu, text="Ver Asistencias", command=self.pantalla_historial_asistencias, width=20).pack(pady=5)
        tk.Button(self.menu, text="Salir", command=self.confirmar_salida, width=20).pack(pady=20)

        # Mostrar pantalla de inicio
        self.pantalla_inicio()

    # Limpia el área dinámica para mostrar nuevas pantallas
    def limpiar_area(self):
        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

    # Pantalla de bienvenida
    def pantalla_inicio(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="¡Bienvenido/a al Sistema del Hospital!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.area_dinamica, text="Este sistema permite registrar trabajadores y tomar asistencias.", font=("Arial", 12)).pack(pady=10)

    # Pantalla para registrar un nuevo trabajador
    def pantalla_registro_trabajador(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registro de Trabajador", font=("Arial", 14, "bold")).pack(pady=10)

        entradas = {}
        campos = ["Nombre", "Edad", "Género", "CURP", "No. de Seguro Social", "No. de Control", "Teléfono", "Domicilio"]

        # Crear campo de entrada para cada dato del trabajador
        def crear_entrada(campo):
            tk.Label(self.area_dinamica, text=f"{campo}:").pack()
            entrada = tk.Entry(self.area_dinamica)
            entrada.pack()
            entradas[campo] = entrada

        for campo in campos:
            crear_entrada(campo)

        # Guardar los datos ingresados
        def guardar_trabajador():
            datos = {campo: entrada.get() for campo, entrada in entradas.items()}
            if not all(datos.values()):
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
                return
            self.trabajadores.append(datos)
            messagebox.showinfo("Guardado", "Trabajador registrado correctamente.")
            self.pantalla_registro_trabajador()

        tk.Button(self.area_dinamica, text="Guardar Trabajador", command=guardar_trabajador).pack(pady=10)

    # Muestra los trabajadores registrados
    def pantalla_historial_trabajadores(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Historial de Trabajadores", font=("Arial", 14, "bold")).pack(pady=10)
        if self.trabajadores:
            for i, t in enumerate(self.trabajadores, 1):
                info = f"{i}. {t['Nombre']}, Edad: {t['Edad']}, Género: {t['Género']}, CURP: {t['CURP']}, No. de Control: {t['No. de Control']}, NSS: {t['No. de Seguro Social']}, Tel: {t['Teléfono']}, Domicilio: {t['Domicilio']}"
                tk.Label(self.area_dinamica, text=info, anchor="w", justify="left").pack()
        else:
            tk.Label(self.area_dinamica, text="No hay trabajadores registrados aún.").pack()

    # Pantalla para registrar la asistencia de un trabajador
    def pantalla_registro_asistencia(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registro de Asistencia", font=("Arial", 14, "bold")).pack(pady=10)

        marco = tk.Frame(self.area_dinamica)
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

        # Función que guarda la asistencia en la lista
        def registrar_asistencia():
            nombre = entry_nombre.get()
            empleado_id = entry_id.get()
            departamento = combo_departamento.get()
            if not nombre or not empleado_id or not departamento:
                messagebox.showwarning("Atención", "Por favor, completa todos los campos.")
                return
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            registro = (nombre, empleado_id, departamento, fecha_hora)
            self.asistencias.append(registro)
            self.actualizar_tabla()

            entry_nombre.delete(0, tk.END)
            entry_id.delete(0, tk.END)
            combo_departamento.set("")

        tk.Button(self.area_dinamica, text="Registrar Asistencia", command=registrar_asistencia).pack(pady=10)

        # Tabla para mostrar asistencias
        self.tabla = ttk.Treeview(self.area_dinamica, columns=("Nombre", "ID", "Departamento", "FechaHora"), show="headings")
        for col in ["Nombre", "ID", "Departamento", "FechaHora"]:
            self.tabla.heading(col, text=col)
        self.tabla.pack(padx=10, pady=10, fill="x")

        self.actualizar_tabla()

    # Muestra el historial completo de asistencias
    def pantalla_historial_asistencias(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Historial de Asistencias", font=("Arial", 14, "bold")).pack(pady=10)

        tabla_local = ttk.Treeview(self.area_dinamica, columns=("Nombre", "ID", "Departamento", "FechaHora"), show="headings")
        for col in ["Nombre", "ID", "Departamento", "FechaHora"]:
            tabla_local.heading(col, text=col)
        tabla_local.pack(padx=10, pady=10, fill="x")

        for registro in self.asistencias:
            tabla_local.insert("", "end", values=registro)

    # Actualiza la tabla de asistencias en la pantalla de registro
    def actualizar_tabla(self):
        if self.tabla:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            for registro in self.asistencias:
                self.tabla.insert("", "end", values=registro)

    # Confirmación antes de cerrar la ventana
    def confirmar_salida(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir del sistema?"):
            self.root.destroy()

# Crear la aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaHospital(root)
    root.mainloop()

       
      
       
