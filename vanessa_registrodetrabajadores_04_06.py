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
registro_vacaciones_frame = None
tabla_trabajadores = None
tabla_asistencia = None
tabla_vacaciones = None
puesto_combo = None

# Datos globales para asistencia
ids_control = []  # Se llenará desde historial_trabajadores
datos_trabajadores = {}  # {id: datos_dict}

# Variables para registro de asistencias
contador_retardos = {}  # {'nc': {'retardo_menor': x, 'retardo_mayor': y, 'faltas': z}}
asistencia_registros = []

# Vacaciones y submódulos
vacaciones_registros = []
dias_economicos_registros = []
periodo_extraordinario_registros = []

# Días festivos ejemplo
dias_festivos = {
    "2025-01-01", "2025-02-03", "2025-03-17", "2025-04-17",
    "2025-04-18", "2025-05-01", "2025-09-16", "2025-11-01",
    "2025-11-02", "2025-11-18", "2025-12-25"
}

# Horarios turnos para asistencia
horarios_turno = {
    "TURNO MATUTINO": ("07:00", "15:00"),
    "TURNO VESPERTINO": ("15:00", "23:00"),
    "TURNO NOCTURNO": ("23:00", "07:00")
}

# --- Ventana principal ---
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

# --- Frame Bienvenida ---
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

# --- Frame Registro Trabajadores ---
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

# --- Frame Registro de Asistencia con lógicas de retardos, faltas y horarios ---
def crear_registro_asistencia_frame():
    global registro_asistencia_frame, tabla_asistencia, lista_ids_cb

    if registro_asistencia_frame is None:
        registro_asistencia_frame = tk.Frame(contenido_dinamico)

        # Variables
        var_id = tk.StringVar()
        var_nombre = tk.StringVar()
        var_departamento = tk.StringVar()
        var_puesto = tk.StringVar()
        var_turno = tk.StringVar()
        var_jornada = tk.StringVar()
        var_horario = tk.StringVar()
        var_estado = tk.StringVar()
        var_fecha = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        var_hora_entrada = tk.StringVar()
        var_hora_salida = tk.StringVar()
        var_horas_extra = tk.StringVar(value="0:00")

        def llenar_campos(event=None):
            nc = var_id.get()
            if nc in datos_trabajadores:
                t = datos_trabajadores[nc]
                var_nombre.set(t.get("Nombre", ""))
                var_departamento.set(t.get("Departamento", ""))
                var_puesto.set(t.get("Puesto", ""))
                var_turno.set(t.get("Turno", ""))
                var_jornada.set(t.get("Jornada", ""))
                var_horario.set(t.get("Horario", ""))
                var_estado.set("")
                var_hora_entrada.set("")
                var_hora_salida.set("")
                var_horas_extra.set("0:00")
            else:
                var_nombre.set("")
                var_departamento.set("")
                var_puesto.set("")
                var_turno.set("")
                var_jornada.set("")
                var_horario.set("")
                var_estado.set("")
                var_hora_entrada.set("")
                var_hora_salida.set("")
                var_horas_extra.set("0:00")

        def calcular_estado_entrada(hora_entrada_str, turno):
            fmt = "%H:%M"
            hora_entrada = datetime.strptime(hora_entrada_str, fmt)
            inicio_str, fin_str = horarios_turno.get(turno, ("07:00", "15:00"))
            inicio = datetime.strptime(inicio_str, fmt)

            # Ajuste nocturno
            if turno == "TURNO NOCTURNO":
                if hora_entrada.hour < 7:
                    inicio = inicio - timedelta(days=1)
                if hora_entrada < inicio:
                    hora_entrada += timedelta(days=1)

            delta_minutos = (hora_entrada - inicio).total_seconds() / 60

            if -10 <= delta_minutos <= 0:
                return "Asistencia"
            elif 0 < delta_minutos <= 10:
                return "Asistencia"
            elif 10 < delta_minutos <= 30:
                return "Retardo menor"
            elif delta_minutos > 30:
                return "Retardo mayor"
            else:
                return "Asistencia"

        def actualizar_contador_retardos(nc, estado):
            if nc not in contador_retardos:
                contador_retardos[nc] = {"retardo_menor": 0, "retardo_mayor": 0, "faltas": 0}

            if estado == "Retardo menor":
                contador_retardos[nc]["retardo_menor"] += 1
                if contador_retardos[nc]["retardo_menor"] >= 3:
                    contador_retardos[nc]["faltas"] += 1
                    contador_retardos[nc]["retardo_menor"] = 0
                    messagebox.showinfo("Falta asignada",
                                        f"Al trabajador {nc} se le asignó 1 falta por 3 retardos menores.")
            elif estado == "Retardo mayor":
                contador_retardos[nc]["retardo_mayor"] += 1
                if contador_retardos[nc]["retardo_mayor"] >= 2:
                    contador_retardos[nc]["faltas"] += 1
                    contador_retardos[nc]["retardo_mayor"] = 0
                    messagebox.showinfo("Falta asignada",
                                        f"Al trabajador {nc} se le asignó 1 falta por 2 retardos mayores.")

        def registrar_entrada():
            nc = var_id.get()
            if nc not in datos_trabajadores:
                messagebox.showerror("Error", "Número de control no registrado")
                return

            ahora = datetime.now()
            hora_entrada_str = ahora.strftime("%H:%M")

            turno = var_turno.get()
            if turno not in horarios_turno:
                messagebox.showerror("Error", "El trabajador no tiene turno válido")
                return

            estado = calcular_estado_entrada(hora_entrada_str, turno)
            var_hora_entrada.set(hora_entrada_str)
            var_estado.set(estado)

            actualizar_contador_retardos(nc, estado)

            messagebox.showinfo("Entrada registrada", f"Entrada registrada a las {hora_entrada_str} con estado: {estado}")

        def registrar_salida():
            nc = var_id.get()
            if nc not in datos_trabajadores:
                messagebox.showerror("Error", "Número de control no registrado")
                return
            if not var_hora_entrada.get():
                messagebox.showwarning("Error", "Primero debe registrar la entrada")
                return

            ahora = datetime.now()
            hora_salida_str = ahora.strftime("%H:%M")
            var_hora_salida.set(hora_salida_str)

            turno = var_turno.get()
            hora_ini_str, hora_fin_str = horarios_turno.get(turno, ("07:00", "15:00"))

            fmt = "%H:%M"
            entrada_dt = datetime.strptime(var_hora_entrada.get(), fmt)
            salida_dt = datetime.strptime(hora_salida_str, fmt)
            fin_dt = datetime.strptime(hora_fin_str, fmt)

            # Ajuste nocturno
            if hora_fin_str == "07:00" and salida_dt < entrada_dt:
                salida_dt += timedelta(days=1)
            if hora_fin_str == "07:00" and fin_dt < entrada_dt:
                fin_dt += timedelta(days=1)

            extra = salida_dt - fin_dt
            horas_extra = "0:00"
            if extra.total_seconds() > 0:
                total_minutos = int(extra.total_seconds() // 60)
                horas = total_minutos // 60
                minutos = total_minutos % 60
                horas_extra = f"{horas}:{minutos:02d}"
            var_horas_extra.set(horas_extra)

            fila = (
                nc,
                var_nombre.get(),
                var_departamento.get(),
                var_puesto.get(),
                var_turno.get(),
                var_jornada.get(),
                var_horario.get(),
                var_fecha.get(),
                var_hora_entrada.get(),
                var_hora_salida.get(),
                var_estado.get(),
                horas_extra
            )
            asistencia_registros.append(fila)
            tabla_asistencia.insert('', 'end', values=fila)

            var_id.set("")
            var_nombre.set("")
            var_departamento.set("")
            var_puesto.set("")
            var_turno.set("")
            var_jornada.set("")
            var_horario.set("")
            var_estado.set("")
            var_hora_entrada.set("")
            var_hora_salida.set("")
            var_horas_extra.set("0:00")

            actualizar_lista_ids()

        def actualizar_lista_ids():
            lista_ids_cb['values'] = ids_control

        # Widgets
        form_frame = ttk.LabelFrame(registro_asistencia_frame, text="Registro de Asistencia")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Número de Control:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lista_ids_cb = ttk.Combobox(form_frame, textvariable=var_id, state="readonly", values=ids_control)
        lista_ids_cb.grid(row=0, column=1, padx=5, pady=5)
        lista_ids_cb.bind("<<ComboboxSelected>>", llenar_campos)

        campos_label = ["Nombre", "Departamento", "Puesto", "Turno", "Jornada", "Horario"]
        vars_campos = [var_nombre, var_departamento, var_puesto, var_turno, var_jornada, var_horario]

        for i, (lbl, varc) in enumerate(zip(campos_label, vars_campos)):
            ttk.Label(form_frame, text=lbl + ":").grid(row=i+1, column=0, padx=5, pady=2, sticky="e")
            ttk.Entry(form_frame, textvariable=varc, state="readonly").grid(row=i+1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Fecha:").grid(row=7, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=var_fecha, state="readonly").grid(row=7, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Hora Entrada:").grid(row=8, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=var_hora_entrada, state="readonly").grid(row=8, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Hora Salida:").grid(row=9, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=var_hora_salida, state="readonly").grid(row=9, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Horas Extra:").grid(row=10, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=var_horas_extra, state="readonly").grid(row=10, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Estado:").grid(row=11, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=var_estado, state="readonly").grid(row=11, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(form_frame, text="Registrar Entrada", command=registrar_entrada).grid(row=12, column=0, padx=10, pady=10)
        ttk.Button(form_frame, text="Registrar Salida", command=registrar_salida).grid(row=12, column=1, padx=10, pady=10)

        tabla_frame = ttk.LabelFrame(registro_asistencia_frame, text="Historial de Asistencias")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                    "Jornada", "Horario", "Fecha", "Hora Entrada", "Hora Salida", "Estado", "Horas Extra")
        tabla_asistencia = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        for col in columnas:
            tabla_asistencia.heading(col, text=col)
            tabla_asistencia.column(col, width=110, anchor="center")

        vscroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_asistencia.yview)
        hscroll = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla_asistencia.xview)
        tabla_asistencia.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        tabla_asistencia.pack(fill="both", expand=True)

def cargar_registro_asistencia():
    ocultar_frames()
    crear_registro_asistencia_frame()
    registro_asistencia_frame.pack(fill="both", expand=True)

    # -- NUEVO Módulo Registro Vacaciones y submódulos --

registro_vacaciones_frame = None

def crear_registro_vacaciones_frame():
    global registro_vacaciones_frame
    if registro_vacaciones_frame is None:
        registro_vacaciones_frame = tk.Frame(contenido_dinamico)

        canvas = tk.Canvas(registro_vacaciones_frame)
        scrollbar = tk.Scrollbar(registro_vacaciones_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        tk.Label(scroll_frame, text="Registro de Vacaciones", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Número de control + autocompletar datos
        tk.Label(scroll_frame, text="Número de Control:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_nc = tk.Entry(scroll_frame)
        entry_nc.grid(row=1, column=1, pady=5)

        campos = ["Nombre", "Departamento", "Puesto", "Turno", "Jornada", "Horario"]
        entradas_autocompletar = {}
        for i, campo in enumerate(campos):
            tk.Label(scroll_frame, text=campo + ":").grid(row=i+2, column=0, sticky="e", padx=5, pady=3)
            ent = tk.Entry(scroll_frame, state="readonly")
            ent.grid(row=i+2, column=1, pady=3, sticky="ew")
            entradas_autocompletar[campo] = ent

        def autocompletar():
            nc = entry_nc.get()
            if nc in datos_trabajadores:
                trabajador = datos_trabajadores[nc]
                for campo in campos:
                    entradas_autocompletar[campo].config(state="normal")
                    entradas_autocompletar[campo].delete(0, tk.END)
                    entradas_autocompletar[campo].insert(0, trabajador.get(campo, ""))
                    entradas_autocompletar[campo].config(state="readonly")
            else:
                messagebox.showerror("Error", "Número de control no encontrado")

        ttk.Button(scroll_frame, text="Buscar", command=autocompletar).grid(row=1, column=2, padx=5)

        # División
        tk.Label(scroll_frame, text="División:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        division_cb = ttk.Combobox(scroll_frame, state="readonly", values=["Primavera", "Invierno"])
        division_cb.grid(row=8, column=1, sticky="ew", pady=5)

        # Quincena
        tk.Label(scroll_frame, text="Quincena:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
        quincena_cb = ttk.Combobox(scroll_frame, state="readonly")
        quincena_cb.grid(row=9, column=1, sticky="ew", pady=5)

        quincenas_primavera = [
            "1-15 Enero", "16-31 Enero",
            "1-15 Febrero", "16-28 Febrero",
            "1-15 Marzo", "16-31 Marzo",
            "1-15 Abril", "16-30 Abril",
            "1-15 Mayo", "16-31 Mayo",
            "1-15 Junio", "16-30 Junio"
        ]
        quincenas_invierno = [
            "1-15 Julio", "16-31 Julio",
            "1-15 Agosto", "16-31 Agosto",
            "1-15 Septiembre", "16-30 Septiembre",
            "1-15 Octubre", "16-31 Octubre",
            "1-15 Noviembre", "16-30 Noviembre",
            "1-15 Diciembre", "16-31 Diciembre"
        ]

        def actualizar_quincenas(event=None):
            if division_cb.get() == "Primavera":
                quincena_cb['values'] = quincenas_primavera
            elif division_cb.get() == "Invierno":
                quincena_cb['values'] = quincenas_invierno
            quincena_cb.set('')

        division_cb.bind("<<ComboboxSelected>>", actualizar_quincenas)

        # Días Económicos
        tk.Label(scroll_frame, text="Días Económicos (máximo 8 días/año):").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        dias_eco_cb = ttk.Combobox(scroll_frame, state="readonly", values=["SI", "NO"])
        dias_eco_cb.grid(row=10, column=1, sticky="ew", pady=5)

        # Períodos Extraordinarios
        tk.Label(scroll_frame, text="Período Extraordinario:").grid(row=11, column=0, sticky="e", padx=5, pady=5)
        periodo_cb = ttk.Combobox(scroll_frame, state="readonly", values=[
            "Alto Riesgo (15 días)", "Mediano Riesgo (8 días)", "Bajo Riesgo (3 días)"])
        periodo_cb.grid(row=11, column=1, sticky="ew", pady=5)

        # Listas para guardar registros
        registros_vacaciones = []
        registros_dias_eco = []
        registros_periodos_ext = []

        def contar_dias_eco(nc):
            return sum(1 for d in registros_dias_eco if d["Número de Control"] == nc)

        def registrar():
            nc = entry_nc.get()
            if nc not in datos_trabajadores:
                messagebox.showerror("Error", "Número de control inválido")
                return

            division = division_cb.get()
            quincena = quincena_cb.get()
            if division == "" or quincena == "":
                messagebox.showwarning("Aviso", "Seleccione división y quincena")
                return

            trabajador = datos_trabajadores[nc]
            jornada = trabajador.get("Jornada", "")
            puesto = trabajador.get("Puesto", "")
            horario = trabajador.get("Horario", "")

            # Validar cupo máximo 3 trabajadores misma jornada, puesto y horario en la quincena
            count = sum(1 for r in registros_vacaciones if
                        r["División"] == division and r["Quincena"] == quincena and
                        r["Jornada"] == jornada and r["Puesto"] == puesto and
                        r["Horario"] == horario)

            if count >= 3:
                messagebox.showwarning("Cupo lleno", "Esta quincena cumplió con su límite de 3 trabajadores para esta jornada, puesto y horario.")
                return

            # Registrar vacaciones
            registro_vac = {
                "Número de Control": nc,
                "Nombre": trabajador.get("Nombre", ""),
                "Departamento": trabajador.get("Departamento", ""),
                "Puesto": puesto,
                "Turno": trabajador.get("Turno", ""),
                "Jornada": jornada,
                "Horario": horario,
                "División": division,
                "Quincena": quincena
            }
            registros_vacaciones.append(registro_vac)
            tree_vac.insert("", "end", values=tuple(registro_vac.values()))

            # Registrar días económicos si es "SI"
            if dias_eco_cb.get() == "SI":
                dias_anteriores = contar_dias_eco(nc)
                if dias_anteriores >= 8:
                    messagebox.showwarning("Límite días económicos", "Ya alcanzó el máximo de 8 días económicos por año.")
                else:
                    fecha = datetime.now().strftime("%Y-%m-%d")
                    registro_eco = {
                        "Número de Control": nc,
                        "Nombre": trabajador.get("Nombre", ""),
                        "Departamento": trabajador.get("Departamento", ""),
                        "Puesto": puesto,
                        "Turno": trabajador.get("Turno", ""),
                        "Jornada": jornada,
                        "Horario": horario,
                        "Fecha": fecha,
                        "Días Económicos Registrados": dias_anteriores + 1
                    }
                    registros_dias_eco.append(registro_eco)
                    tree_eco.insert("", "end", values=tuple(registro_eco.values()))

            # Registrar período extraordinario si seleccionado
            pe = periodo_cb.get()
            if pe != "":
                dias_pe = 0
                if "Alto" in pe:
                    dias_pe = 15
                elif "Mediano" in pe:
                    dias_pe = 8
                elif "Bajo" in pe:
                    dias_pe = 3
                registro_pe = {
                    "Número de Control": nc,
                    "Nombre": trabajador.get("Nombre", ""),
                    "Departamento": trabajador.get("Departamento", ""),
                    "Puesto": puesto,
                    "Turno": trabajador.get("Turno", ""),
                    "Jornada": jornada,
                    "Horario": horario,
                    "Nivel de Riesgo": pe,
                    "Días": dias_pe,
                    "Fecha Registro": datetime.now().strftime("%Y-%m-%d")
                }
                registros_periodos_ext.append(registro_pe)
                tree_pe.insert("", "end", values=tuple(registro_pe.values()))

            messagebox.showinfo("Registrado", "Vacaciones y submódulos registrados correctamente.")

            # Limpiar campos
            entry_nc.delete(0, tk.END)
            for ent in entradas_autocompletar.values():
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.config(state="readonly")
            division_cb.set('')
            quincena_cb.set('')
            dias_eco_cb.set('')
            periodo_cb.set('')

        ttk.Button(scroll_frame, text="Registrar", command=registrar).grid(row=12, column=0, columnspan=3, pady=15)

        # Tablas historial Vacaciones, Días Económicos y Períodos Extraordinarios
        # Vacaciones
        tk.Label(scroll_frame, text="Historial Vacaciones").grid(row=13, column=0, columnspan=4, pady=5)
        columns_vac = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                       "Jornada", "Horario", "División", "Quincena")
        tree_vac = ttk.Treeview(scroll_frame, columns=columns_vac, show="headings", height=7)
        for col in columns_vac:
            tree_vac.heading(col, text=col)
            tree_vac.column(col, width=120, anchor="center")
        tree_vac.grid(row=14, column=0, columnspan=4, pady=5, sticky="ew")

        # Días Económicos
        tk.Label(scroll_frame, text="Historial Días Económicos").grid(row=15, column=0, columnspan=4, pady=5)
        columns_eco = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                       "Jornada", "Horario", "Fecha", "Días Económicos Registrados")
        tree_eco = ttk.Treeview(scroll_frame, columns=columns_eco, show="headings", height=5)
        for col in columns_eco:
            tree_eco.heading(col, text=col)
            tree_eco.column(col, width=120, anchor="center")
        tree_eco.grid(row=16, column=0, columnspan=4, pady=5, sticky="ew")

        # Períodos Extraordinarios
        tk.Label(scroll_frame, text="Historial Períodos Extraordinarios").grid(row=17, column=0, columnspan=4, pady=5)
        columns_pe = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                      "Jornada", "Horario", "Nivel de Riesgo", "Días", "Fecha Registro")
        tree_pe = ttk.Treeview(scroll_frame, columns=columns_pe, show="headings", height=5)
        for col in columns_pe:
            tree_pe.heading(col, text=col)
            tree_pe.column(col, width=110, anchor="center")
        tree_pe.grid(row=18, column=0, columnspan=4, pady=5, sticky="ew")

def cargar_registro_vacaciones():
    ocultar_frames()
    crear_registro_vacaciones_frame()
    registro_vacaciones_frame.pack(fill="both", expand=True)

# -- Botones menú lateral --

btn_bienvenida = tk.Button(menu_lateral, text="Bienvenida", command=cargar_bienvenida)
btn_bienvenida.pack(fill="x", pady=5)

btn_registro_trab = tk.Button(menu_lateral, text="Registro Trabajadores", command=cargar_registro_trabajadores)
btn_registro_trab.pack(fill="x", pady=5)

btn_registro_asistencia = tk.Button(menu_lateral, text="Registro Asistencia", command=cargar_registro_asistencia)
btn_registro_asistencia.pack(fill="x", pady=5)

btn_registro_vacaciones = tk.Button(menu_lateral, text="Registro Vacaciones", command=cargar_registro_vacaciones)
btn_registro_vacaciones.pack(fill="x", pady=5)

btn_salir = tk.Button(menu_lateral, text="Salir", command=ventana.quit)
btn_salir.pack(fill="x", pady=5)

# Carga inicial
cargar_bienvenida()

ventana.mainloop()
