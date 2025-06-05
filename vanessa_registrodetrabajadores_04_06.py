
import tkinter as tk
from tkinter import ttk, messagebox

# Diccionario de puestos por departamento (se mantiene igual)
puestos_por_departamento = {
    "Departamentos Médicos Asistenciales": [
        "Medicina Interna", "Pediatría", "Ginecología y Obstetricia", "Cirugía General",
        "Urgencias o Emergencias", "Traumatología y Ortopedia", "Cardiología", "Neurología",
        "Psiquiatría y Salud Mental", "Oncología", "Urología", "Dermatología", "Oftalmología",
        "Otorrinolaringología (ORL)", "Anestesiología y Reanimación"
    ],
    "Departamentos de Apoyo Diagnóstico y Terapéutico": [
        "Laboratorio Clínico", "Imagenología", "Farmacia Hospitalaria", "Banco de Sangre",
        "Rehabilitación Física y Terapia Ocupacional", "Nutrición y Dietética", "Endoscopía", "Patología"
    ],
    "Departamentos de Enfermería": [
        "Enfermería General", "Cuidados Intensivos", "Pediatría (enfermería pediátrica)", "Sala de Partos y Neonatología"
    ],
    "Departamentos Administrativos": [
        "Admisión y Registro", "Recursos Humanos", "Finanzas y Contabilidad", "Compras y Almacén",
        "Tecnologías de la Información (TI)", "Trabajo Social", "Archivo Clínico o Historias Médicas",
        "Calidad y Seguridad del Paciente"
    ],
    "Departamentos Generales o de Apoyo Operativo": [
        "Limpieza y Mantenimiento", "Lavandería", "Cocina y Alimentación", "Seguridad y Vigilancia",
        "Transporte Interno de Pacientes", "Gestión Ambiental y Residuos Hospitalarios"
    ]
}

cupo_jornada = {}
historial_trabajadores = [] # Esta lista seguirá guardando tus datos

# Variables globales para los frames de cada sección
bienvenida_frame = None
registro_trabajadores_frame = None
tabla_frame = None # Mantener esta para la tabla de historial

# Variables globales para la tabla y sus entradas (necesarias para actualizar y acceder)
tabla = None
puesto_combo = None # Necesario para actualizar sus valores

ventana = tk.Tk()
ventana.title("Sistema Hospitalario")
ventana.geometry("1200x800")

menu_lateral = tk.Frame(ventana, width=200, bg="#d9d9d9")
menu_lateral.pack(side="left", fill="y")

contenido_dinamico = tk.Frame(ventana)
contenido_dinamico.pack(side="right", fill="both", expand=True)

# Función para ocultar todos los frames en contenido_dinamico
def ocultar_frames():
    for frame in contenido_dinamico.winfo_children():
        frame.pack_forget()

# --- Pantalla de Bienvenida ---
def crear_bienvenida_frame():
    global bienvenida_frame
    if bienvenida_frame is None:
        bienvenida_frame = tk.Frame(contenido_dinamico, bg="#f0f0f0")

        mensaje = tk.Label(
            bienvenida_frame,
            text="Bienvenido al Sistema Hospitalario",
            font=("Helvetica", 24, "bold"),
            fg="#2b2b2b",
            bg="#f0f0f0"
        )
        mensaje.pack(pady=100)

        subtitulo = tk.Label(
            bienvenida_frame,
            text="Seleccione una opción del menú para comenzar",
            font=("Helvetica", 14),
            fg="#444",
            bg="#f0f0f0"
        )
        subtitulo.pack()
    
def cargar_bienvenida():
    ocultar_frames()
    crear_bienvenida_frame() # Asegura que el frame de bienvenida esté creado
    bienvenida_frame.pack(expand=True, fill="both")
    bienvenida_frame.lift() # Asegura que esté al frente

# --- Registro de Trabajadores ---
def crear_registro_trabajadores_frame():
    global registro_trabajadores_frame, tabla, tabla_frame, puesto_combo # Asegura acceso a globales

    if registro_trabajadores_frame is None:
        registro_trabajadores_frame = tk.Frame(contenido_dinamico)

        datos = {
            "Nombre": tk.StringVar(),
            "Edad": tk.StringVar(),
            "CURP": tk.StringVar(),
            "NSS": tk.StringVar(),
            "Domicilio": tk.StringVar(),
            "Teléfono": tk.StringVar(),
            "Número de control": tk.StringVar(),
            "Género": tk.StringVar(),
            "Turno": tk.StringVar(),
            "Horario": tk.StringVar(),
            "Departamento": tk.StringVar(),
            "Puesto": tk.StringVar(),
            "Jornada": tk.StringVar(),
            "Fecha de Nacimiento": tk.StringVar(),
            "Tipo de Contratación": tk.StringVar(),
            "Último Grado de Estudios": tk.StringVar(),
            "Correo Electrónico": tk.StringVar(),
            "Cédula Profesional": tk.StringVar(),
            "Fecha de Ingreso": tk.StringVar()
        }

        def actualizar_puestos(*args):
            depto = datos["Departamento"].get()
            puestos = puestos_por_departamento.get(depto, [])
            puesto_combo['values'] = puestos
            datos["Puesto"].set('')

        def validar_datos():
            obligatorios = list(datos.keys())
            for campo in obligatorios:
                if not datos[campo].get().strip():
                    messagebox.showwarning("Campo vacío", f"El campo '{campo}' es obligatorio.")
                    return False

            if len(datos["CURP"].get().strip()) > 18:
                messagebox.showerror("CURP inválido", "El CURP no debe tener más de 18 caracteres.")
                return False
            if not datos["Teléfono"].get().isdigit() or len(datos["Teléfono"].get()) > 10:
                messagebox.showerror("Teléfono inválido", "El teléfono debe tener hasta 10 dígitos numéricos.")
                return False
            if not datos["NSS"].get().isdigit() or len(datos["NSS"].get()) > 11:
                messagebox.showerror("NSS inválido", "El NSS debe tener hasta 11 dígitos numéricos.")
                return False
            if not datos["Número de control"].get().isdigit() or len(datos["Número de control"].get()) > 10:
                messagebox.showerror("Número de control inválido", "Debe ser numérico y hasta 10 dígitos.")
                return False
            if not datos["Cédula Profesional"].get().isdigit() or len(datos["Cédula Profesional"].get()) > 10:
                messagebox.showerror("Cédula inválida", "La cédula profesional debe ser numérica y de máximo 10 dígitos.")
                return False

            return True

        def registrar_trabajador():
            if not validar_datos():
                return

            jornada = datos["Jornada"].get()
            puesto = datos["Puesto"].get()
            clave = f"{puesto}_{jornada}"

            if not puesto or not jornada:
                messagebox.showwarning("Campos incompletos", "Seleccione puesto y jornada")
                return

            if cupo_jornada.get(clave, 0) >= 10:
                messagebox.showerror("Cupo lleno", "Esta jornada ha llegado al límite de trabajadores.")
                return

            valores_trabajador = [v.get() for v in datos.values()]
            historial_trabajadores.append(valores_trabajador) # Agrega los datos a la lista global

            cupo_jornada[clave] = cupo_jornada.get(clave, 0) + 1

            for var in datos.values():
                var.set('')
            puesto_combo['values'] = [] # Limpia los valores del combobox de puesto

            actualizar_tabla_historial() # Llama a la función para refrescar la tabla

        entrada_frame = ttk.LabelFrame(registro_trabajadores_frame, text="Datos del Trabajador")
        entrada_frame.pack(padx=10, pady=10, fill="x", expand=False)

        num_campos_por_columna = (len(datos) + 1) // 2

        etiquetas = list(datos.keys())
        for i, etiqueta in enumerate(etiquetas):
            row = i % num_campos_por_columna
            col = (i // num_campos_por_columna) * 2

            ttk.Label(entrada_frame, text=etiqueta).grid(row=row, column=col, sticky="e", padx=5, pady=2)

            if etiqueta == "Género":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["FEMENINO", "MASCULINO", "OTRO"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Turno":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["TURNO MATUTINO", "TURNO VESPERTINO", "TURNO NOCTURNO"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Horario":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["07:00 a 15:00", "15:00 a 23:00", "23:00 a 07:00"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Departamento":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=list(puestos_por_departamento.keys()))
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
                combo.bind("<<ComboboxSelected>>", actualizar_puestos)
            elif etiqueta == "Puesto":
                puesto_combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly")
                puesto_combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Jornada":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["LUNES A VIERNES", "LUNES, MIÉRCOLES, VIERNES",
                                             "MARTES Y JUEVES", "SÁBADOS Y DOMINGOS", "DOMINGOS",
                                             "SÁBADOS, DOMINGOS, DÍAS FECTIVOS",
                                             "MIÉRCOLES, JUEVES, VIERNES, SÁBADOS, DOMINGOS",
                                             "MARTES, JUEVES, SÁBADOS"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Tipo de Contratación":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["BASIFICADOS", "HOMOLOGADOS", "REGULARIZADOS", "CONTRATO", "SUPLENTES O CUBREINCIDENCIAS", "OTRO"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Último Grado de Estudios":
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly",
                                     values=["EDUCACIÓN BÁSICA", "EDUCACIÓN MEDIA SUPERIOR", "EDUCACIÓN SUPERIOR"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            else:
                ttk.Entry(entrada_frame, textvariable=datos[etiqueta]).grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")

        entrada_frame.grid_columnconfigure(1, weight=1)
        entrada_frame.grid_columnconfigure(3, weight=1)

        ttk.Button(entrada_frame, text="Registrar Trabajador", command=registrar_trabajador).grid(row=num_campos_por_columna, column=0, columnspan=4, pady=10)

        # Creación de la tabla de historial (solo una vez)
        tabla_frame = ttk.LabelFrame(registro_trabajadores_frame, text="Historial de Trabajadores")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = etiquetas
        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        vscroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        vscroll.pack(side="right", fill="y")
        tabla.configure(yscrollcommand=vscroll.set)

        hscroll = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)
        hscroll.pack(side="bottom", fill="x")
        tabla.configure(xscrollcommand=hscroll.set)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="w")
            
        tabla.pack(fill="both", expand=True)

# Función para actualizar la tabla con los datos del historial
def actualizar_tabla_historial():
    global tabla
    if tabla is not None: # Asegúrate de que la tabla exista antes de intentar actualizarla
        for item in tabla.get_children():
            tabla.delete(item)
        
        for registro in historial_trabajadores:
            tabla.insert('', 'end', values=registro)

def cargar_registro_trabajadores():
    ocultar_frames()
    crear_registro_trabajadores_frame() # Asegura que el frame de registro esté creado
    registro_trabajadores_frame.pack(expand=True, fill="both")
    registro_trabajadores_frame.lift() # Asegura que esté al frente
    actualizar_tabla_historial() # Carga los datos al mostrar la pantalla

# --- Botones del Menú Lateral ---
ttk.Button(menu_lateral, text="Bienvenida", command=cargar_bienvenida).pack(pady=10, padx=10, fill="x")
ttk.Button(menu_lateral, text="Registro de Trabajadores", command=cargar_registro_trabajadores).pack(pady=10, padx=10, fill="x")

# Mostrar bienvenida al inicio
cargar_bienvenida()

ventana.mainloop()