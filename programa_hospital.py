import tkinter as tk
from tkinter import messagebox

class Trabajador:
    def __init__(self, nombre, edad, genero, curp, nss, control, telefono, domicilio):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.curp = curp
        self.nss = nss
        self.control = control
        self.telefono = telefono
        self.domicilio = domicilio

    def __str__(self):
        return (f"{self.nombre} - Edad: {self.edad} - Género: {self.genero} - CURP: {self.curp} - "
                f"NSS: {self.nss} - Número de control: {self.control} - "
                f"Teléfono: {self.telefono} - Domicilio: {self.domicilio}")

class AppHospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Trabajadores")
        self.root.geometry("600x500")
        self.root.config(bg="lightblue")

        self.trabajadores = []

        self.menu = tk.Frame(root, bg="lightblue", width=150)
        self.menu.pack(side="left", fill="y")

        self.area_dinamica = tk.Frame(root, bg="white")
        self.area_dinamica.pack(side="right", expand=True, fill="both")

        self.crear_menu()
        self.pantalla_inicio()

    def limpiar_area_dinamica(self):
        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

    def crear_menu(self):
        tk.Button(self.menu, text="Bienvenida", command=self.pantalla_inicio, width=18).pack(pady=5)
        tk.Button(self.menu, text="Registrar", command=self.pantalla_registro, width=18).pack(pady=5)
        tk.Button(self.menu, text="Trabajadores", command=self.pantalla_historial, width=18).pack(pady=20)
        tk.Button(self.menu, text="Salir", command=self.root.destroy, width=18).pack(pady=30)

    def pantalla_inicio(self):
        self.limpiar_area_dinamica()
        tk.Label(self.area_dinamica, text="¡Bienvenido/a!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.area_dinamica, text="Hola, esta aplicación lleva el control del registro de los trabajadores de este hospital.", font=("Arial", 12)).pack(pady=10)

    def pantalla_registro(self):
        self.limpiar_area_dinamica()
        tk.Label(self.area_dinamica, text="Datos del trabajador", font=("Arial", 14, "bold")).pack(pady=10)

        campos = [
            "Nombre", "Edad", "Género", "CURP", "No. de Seguro Social",
            "No. de Control", "Teléfono", "Domicilio"
        ]
        self.entradas = {}

        for campo in campos:
            tk.Label(self.area_dinamica, text=f"{campo}:").pack()
            entrada = tk.Entry(self.area_dinamica)
            entrada.pack()
            self.entradas[campo] = entrada

        tk.Button(self.area_dinamica, text="Guardar datos", command=self.guardar_datos).pack(pady=10)

    def guardar_datos(self):
        datos = {campo: entrada.get() for campo, entrada in self.entradas.items()}

        if not all(datos.values()):
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return

       

        nuevo_trabajador = Trabajador(
            datos["Nombre"],
            datos["Edad"], 
            datos["Género"],
            datos["CURP"],
            datos["No. de Seguro Social"],
            datos["No. de Control"],
            datos["Teléfono"],
            datos["Domicilio"]
        )

        self.trabajadores.append(nuevo_trabajador)
        messagebox.showinfo("Guardado", "Datos del trabajador guardados correctamente.")

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def pantalla_historial(self):
        self.limpiar_area_dinamica()
        tk.Label(self.area_dinamica, text="Historial de Trabajadores", font=("Arial", 14, "bold")).pack(pady=10)

        if self.trabajadores:
            for i, t in enumerate(self.trabajadores, 1):
                tk.Label(self.area_dinamica, text=f"{i}. {str(t)}", anchor="w", justify="left", wraplength=550).pack()
        else:
            tk.Label(self.area_dinamica, text="No hay trabajadores registrados aún.").pack()

# Crear la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppHospital(ventana)
    ventana.mainloop()
    
