import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# -- Datos y estructuras --

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
historial_trabajadores = []

# Variables globales para frames y componentes
bienvenida_frame = None
registro_trabajadores_frame = None
registro_asistencia_frame = None
tabla_trabajadores = None
tabla_asistencia = None
puesto_combo = None

# Datos globales para asistencia
ids_control = []  # Se llenará desde historial_trabajadores
datos_trabajadores = {}  # {id: datos_dict}
retardos_menores = {}
retardos_mayores = {}

dias_festivos = {
    "2025-01-01", "2025-02-03", "2025-03-17", "2025-04-17",
    "2025-04-18", "2025-05-01", "2025-09-16", "2025-11-01",
    "2025-11-02", "2025-11-18", "2025-12-25"
}

horarios_turno = {
    "TURNO MATUTINO": ("07:00", "15:00"),
    "TURNO VESPERTINO": ("15:00", "23:00"),
    "TURNO NOCTURNO": ("23:00", "07:00")
}

# -- Ventana principal --

ventana = tk.Tk()
ventana.title("Sistema Hospitalario")
ventana.geometry("1200x800")

menu_lateral = tk.Frame(ventana, width=200, bg="#d9d9d9")
menu_lateral.pack(side="left", fill="y")

contenido_dinamico = tk.Frame(ventana)
contenido_dinamico.pack(side="right", fill="both", expand=True)

def ocultar_frames():
    for frame in contenido_dinamico.winfo_children():
        frame.pack_forget()

# -- Frame Bienvenida --

def crear_bienvenida_frame():
    global bienvenida_frame
    if bienvenida_frame is None:
        bienvenida_frame = tk.Frame(contenido_dinamico, bg="#f0f0f0")
        tk.Label(bienvenida_frame, text="Bienvenido al Sistema Hospitalario",
                 font=("Helvetica", 24, "bold"), fg="#2b2b2b", bg="#f0f0f0").pack(pady=100)
        tk.Label(bienvenida_frame, text="Seleccione una opción del menú para comenzar",
                 font=("Helvetica", 14), fg="#444", bg="#f0f0f0").pack()

def cargar_bienvenida():
    ocultar_frames()
    crear_bienvenida_frame()
    bienvenida_frame.pack(expand=True, fill="both")

# -- Frame Registro Trabajadores --

def crear_registro_trabajadores_frame():
    global registro_trabajadores_frame, tabla_trabajadores, puesto_combo, ids_control, datos_trabajadores

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
            for campo, var in datos.items():
                if not var.get().strip():
                    messagebox.showwarning("Campo vacío", f"El campo '{campo}' es obligatorio.")
                    return False
            return True

        def registrar_trabajador():
            if not validar_datos():
                return
            jornada = datos["Jornada"].get()
            puesto = datos["Puesto"].get()
            clave = f"{puesto}_{jornada}"
            if cupo_jornada.get(clave, 0) >= 10:
                messagebox.showerror("Cupo lleno", "Esta jornada ha llegado al límite de trabajadores.")
                return
            registro = {k: v.get() for k, v in datos.items()}
            historial_trabajadores.append(registro)
            cupo_jornada[clave] = cupo_jornada.get(clave, 0) + 1
            # Actualizar IDs y datos para asistencias
            ids_control.clear()
            datos_trabajadores.clear()
            for t in historial_trabajadores:
                ids_control.append(t["Número de control"])
                datos_trabajadores[t["Número de control"]] = t

            for var in datos.values():
                var.set('')
            puesto_combo['values'] = []
            actualizar_tabla_historial()

        entrada_frame = ttk.LabelFrame(registro_trabajadores_frame, text="Datos del Trabajador")
        entrada_frame.pack(padx=10, pady=10, fill="x")

        num_campos_por_columna = (len(datos) + 1) // 2
        etiquetas = list(datos.keys())

        for i, etiqueta in enumerate(etiquetas):
            row = i % num_campos_por_columna
            col = (i // num_campos_por_columna) * 2
            ttk.Label(entrada_frame, text=etiqueta).grid(row=row, column=col, sticky="e", padx=5, pady=2)

            if etiqueta in ["Género", "Turno", "Horario", "Departamento", "Jornada", "Tipo de Contratación", "Último Grado de Estudios"]:
                combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly")
                if etiqueta == "Género":
                    combo['values'] = ["FEMENINO", "MASCULINO", "OTRO"]
                elif etiqueta == "Turno":
                    combo['values'] = ["TURNO MATUTINO", "TURNO VESPERTINO", "TURNO NOCTURNO"]
                elif etiqueta == "Horario":
                    combo['values'] = ["07:00 a 15:00", "15:00 a 23:00", "23:00 a 07:00"]
                elif etiqueta == "Departamento":
                    combo['values'] = list(puestos_por_departamento.keys())
                    combo.bind("<<ComboboxSelected>>", actualizar_puestos)
                elif etiqueta == "Jornada":
                    combo['values'] = ["LUNES A VIERNES", "LUNES, MIÉRCOLES, VIERNES", "MARTES Y JUEVES",
                                       "SÁBADOS Y DOMINGOS", "DOMINGOS", "SÁBADOS, DOMINGOS, DÍAS FECTIVOS",
                                       "MIÉRCOLES, JUEVES, VIERNES, SÁBADOS, DOMINGOS", "MARTES, JUEVES, SÁBADOS"]
                elif etiqueta == "Tipo de Contratación":
                    combo['values'] = ["BASIFICADOS", "HOMOLOGADOS", "REGULARIZADOS", "CONTRATO", "SUPLENTES O CUBREINCIDENCIAS", "OTRO"]
                elif etiqueta == "Último Grado de Estudios":
                    combo['values'] = ["EDUCACIÓN BÁSICA", "EDUCACIÓN MEDIA SUPERIOR", "EDUCACIÓN SUPERIOR"]
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
                if etiqueta == "Puesto":
                    puesto_combo = combo
            elif etiqueta == "Puesto":
                puesto_combo = ttk.Combobox(entrada_frame, textvariable=datos[etiqueta], state="readonly")
                puesto_combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            else:
                ttk.Entry(entrada_frame, textvariable=datos[etiqueta]).grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")

        ttk.Button(entrada_frame, text="Registrar Trabajador", command=registrar_trabajador).grid(
            row=num_campos_por_columna+1, column=0, columnspan=4, pady=10)

        tabla_frame = ttk.LabelFrame(registro_trabajadores_frame, text="Historial de Trabajadores")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = etiquetas
        tabla_trabajadores = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        for col in columnas:
            tabla_trabajadores.heading(col, text=col)
            tabla_trabajadores.column(col, width=150, anchor="w")

        vscroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_trabajadores.yview)
        hscroll = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla_trabajadores.xview)
        tabla_trabajadores.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        tabla_trabajadores.pack(fill="both", expand=True)

def actualizar_tabla_historial():
    if tabla_trabajadores:
        tabla_trabajadores.delete(*tabla_trabajadores.get_children())
        for registro in historial_trabajadores:
            valores = [registro.get(col, "") for col in tabla_trabajadores["columns"]]
            tabla_trabajadores.insert('', 'end', values=valores)

def cargar_registro_trabajadores():
    ocultar_frames()
    crear_registro_trabajadores_frame()
    registro_trabajadores_frame.pack(expand=True, fill="both")
    actualizar_tabla_historial()

# -- Frame Registro de Asistencia --

registro_actual = {"entrada": None, "salida": None}  # Para controlar registros

def crear_registro_asistencia_frame():
    global registro_asistencia_frame, tabla_asistencia, combo_id, entradas

    if registro_asistencia_frame is None:
        registro_asistencia_frame = tk.Frame(contenido_dinamico)

        titulo = tk.Label(registro_asistencia_frame, text="REGISTRO DE ASISTENCIA", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = tk.Frame(registro_asistencia_frame)
        frame.pack(pady=10)

        tk.Label(frame, text="Número de Control:").grid(row=0, column=0, sticky="e")
        combo_id = ttk.Combobox(frame, values=ids_control, state="readonly")
        combo_id.grid(row=0, column=1, padx=5, pady=2)

        entradas = {}
        campos = ["Nombre", "Número de Control", "Departamento", "Turno", "Jornada", "Horario"]
        for i, campo in enumerate(campos, 1):
            tk.Label(frame, text=f"{campo}:").grid(row=i, column=0, sticky="e")
            entrada = tk.Entry(frame, state="readonly")
            entrada.grid(row=i, column=1, padx=5, pady=2)
            entradas[campo] = entrada

        # Tabla de historial
        columnas = ("Fecha", "Entrada", "Salida", "Tipo")
        tabla_asistencia = ttk.Treeview(registro_asistencia_frame, columns=columnas, show="headings")
        for col in columnas:
            tabla_asistencia.heading(col, text=col)
            tabla_asistencia.column(col, width=150, anchor="w")
        tabla_asistencia.pack(pady=10, fill="both", expand=True)

        # Botones
        btn_entrada = tk.Button(frame, text="Registrar Entrada", command=registrar_entrada)
        btn_entrada.grid(row=7, column=0, pady=5)

        btn_salida = tk.Button(frame, text="Registrar Salida", command=registrar_salida)
        btn_salida.grid(row=7, column=1, pady=5)

        combo_id.bind("<<ComboboxSelected>>", cargar_datos)

def cargar_datos(event=None):
    id_sel = combo_id.get()
    if id_sel in datos_trabajadores:
        datos = datos_trabajadores[id_sel]
        for campo in entradas:
            valor = datos.get(campo, "")
            entradas[campo].config(state="normal")
            entradas[campo].delete(0, tk.END)
            entradas[campo].insert(0, valor)
            entradas[campo].config(state="readonly")

def es_dia_festivo():
    hoy = datetime.now().strftime("%Y-%m-%d")
    return hoy in dias_festivos

def registrar_entrada():
    id_sel = combo_id.get()
    if not id_sel:
        messagebox.showwarning("Advertencia", "Seleccione un número de control.")
        return

    datos = datos_trabajadores[id_sel]
    turno = datos["Turno"]
    jornada = datos["Jornada"]
    horario_inicio_str, horario_fin_str = horarios_turno.get(turno, ("00:00", "00:00"))

    ahora = datetime.now()
    fecha_actual = ahora.strftime("%Y-%m-%d")
    hora_actual = ahora.strftime("%H:%M")

    if es_dia_festivo() and "DÍAS FECTIVOS" not in jornada:
        tipo = "Descanso"
    else:
        hora_inicio = datetime.strptime(horario_inicio_str, "%H:%M")
        hora_actual_dt = datetime.strptime(hora_actual, "%H:%M")

        if hora_actual_dt <= hora_inicio:
            tipo = "Asistencia"
        elif hora_inicio < hora_actual_dt <= hora_inicio + timedelta(minutes=10):
            tipo = "Asistencia con tolerancia"
        elif hora_inicio + timedelta(minutes=10) < hora_actual_dt <= hora_inicio + timedelta(minutes=30):
            tipo = "Retardo Menor"
            retardos_menores[id_sel] = retardos_menores.get(id_sel, 0) + 1
        else:
            tipo = "Retardo Mayor"
            retardos_mayores[id_sel] = retardos_mayores.get(id_sel, 0) + 1

        # Verificar faltas por acumulación
        if retardos_menores.get(id_sel, 0) >= 3:
            tipo = "FALTA (3 retardos menores)"
            retardos_menores[id_sel] = 0
        elif retardos_mayores.get(id_sel, 0) >= 2:
            tipo = "FALTA (2 retardos mayores)"
            retardos_mayores[id_sel] = 0

    registro_actual["entrada"] = ahora.strftime("%H:%M")
    tabla_asistencia.insert("", "end", values=(fecha_actual, registro_actual["entrada"], "", tipo))
    messagebox.showinfo("Entrada Registrada", f"{tipo} registrada para {datos['Nombre']}.")

def registrar_salida():
    if not registro_actual["entrada"]:
        messagebox.showwarning("Advertencia", "Primero debe registrar la entrada.")
        return
    salida = datetime.now().strftime("%H:%M")
    registro_actual["salida"] = salida

    items = tabla_asistencia.get_children()
    if items:
        ultima = items[-1]
        valores = tabla_asistencia.item(ultima)["values"]
        nuevos_valores = valores[:2] + [salida] + valores[3:]
        tabla_asistencia.item(ultima, values=nuevos_valores)
        messagebox.showinfo("Salida Registrada", "Hora de salida registrada correctamente.")

def mostrar_registro_asistencia():
    ocultar_frames()
    crear_registro_asistencia_frame()
    registro_asistencia_frame.pack(expand=True, fill="both")

# -- Botones menú lateral --

tk.Button(menu_lateral, text="Inicio", width=25, command=cargar_bienvenida).pack(pady=10)
tk.Button(menu_lateral, text="Registro de Trabajadores", width=25, command=cargar_registro_trabajadores).pack(pady=10)
tk.Button(menu_lateral, text="Registro de Asistencia", width=25, command=mostrar_registro_asistencia).pack(pady=10)
tk.Button(menu_lateral, text="Salir", width=25, command=ventana.quit).pack(side="bottom", pady=10)

cargar_bienvenida()
ventana.mainloop()
