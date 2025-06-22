import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# --- Gestión de Datos (Mejor encapsulado) ---
class HospitalData:
    def __init__(self):
        self.puestos_por_departamento = {
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
        self.cupo_jornada = {}
        self.historial_trabajadores = []
        self.asistencia_registros = []
        self.vacaciones_registros = []
        self.dias_economicos_registros = []
        self.periodo_extraordinario_registros = []
        self.contador_retardos = {} # {'nc': {'retardo_menor': x, 'retardo_mayor': y, 'faltas': z}}
        self.datos_trabajadores = {} # {id: datos_dict}
        self.ids_control = [] # Lista para los números de control

        self.dias_festivos = { # Ejemplo de días festivos
            "2025-01-01", "2025-02-03", "2025-03-17", "2025-04-17",
            "2025-04-18", "2025-05-01", "2025-09-16", "2025-11-01",
            "2025-11-02", "2025-11-18", "2025-12-25"
        }

        self.horarios_turno = { # Horarios de turnos para asistencia
            "TURNO MATUTINO": ("07:00", "15:00"),
            "TURNO VESPERTINO": ("15:00", "23:00"),
            "TURNO NOCTURNO": ("23:00", "07:00")
        }

# --- Clase Padre: BaseModule ---
class BaseModule:
    def __init__(self, parent_frame, app_instance, data_store):
        self.parent_frame = parent_frame
        self.app = app_instance
        self.data = data_store
        self.frame = None

    def hide(self):
        if self.frame:
            self.frame.pack_forget()

    def show(self):
        raise NotImplementedError("El método 'show' debe ser implementado por las clases hijas.")

    def create_labeled_frame(self, parent, text_label):
        return ttk.LabelFrame(parent, text=text_label)

    def create_treeview_with_scroll(self, parent, columns, heights=5):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=heights)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        vscroll = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hscroll = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

        return tree, vscroll, hscroll

# --- Clase Hijo 1: BienvenidaModule ---
class BienvenidaModule(BaseModule):
    def __init__(self, parent_frame, app_instance, data_store):
        super().__init__(parent_frame, app_instance, data_store)
        self.frame = tk.Frame(self.parent_frame, bg="#f0f0f0")
        # --- MODIFICACIÓN AQUÍ: Una sola etiqueta de bienvenida ---
        self.welcome_label = tk.Label(self.frame,
                                     text="HOSPITAL RÍOS\nBienvenido al Sistema Hospitalario\n\nSeleccione una opción del menú para comenzar",
                                     font=("Helvetica", 24, "bold"), fg="#2b2b2b", bg="#f0f0f0", justify="center")
        self.welcome_label.pack(pady=100) # La etiqueta se empaqueta aquí al inicializar el módulo.

    def show(self):
        # Solo necesitamos empaquetar el frame principal, ya que la etiqueta está dentro.
        self.frame.pack(expand=True, fill="both")

# --- Clase Hijo 2: RegistroTrabajadoresModule ---
class RegistroTrabajadoresModule(BaseModule):
    def __init__(self, parent_frame, app_instance, data_store):
        super().__init__(parent_frame, app_instance, data_store)
        self.frame = tk.Frame(self.parent_frame)
        self.puesto_combo = None
        self.tabla_trabajadores = None

        self.datos_entrada = {
            "Nombre": tk.StringVar(), "Edad": tk.StringVar(), "CURP": tk.StringVar(),
            "NSS": tk.StringVar(), "Domicilio": tk.StringVar(), "Teléfono": tk.StringVar(),
            "Número de control": tk.StringVar(), "Género": tk.StringVar(), "Turno": tk.StringVar(),
            "Horario": tk.StringVar(), "Departamento": tk.StringVar(), "Puesto": tk.StringVar(),
            "Jornada": tk.StringVar(), "Fecha de Nacimiento": tk.StringVar(),
            "Tipo de Contratación": tk.StringVar(), "Último Grado de Estudios": tk.StringVar(),
            "Correo Electrónico": tk.StringVar(), "Cédula Profesional": tk.StringVar(),
            "Fecha de Ingreso": tk.StringVar()
        }
        self._create_widgets()

    def _create_widgets(self):
        entrada_frame = self.create_labeled_frame(self.frame, "Datos del Trabajador")
        entrada_frame.pack(padx=10, pady=10, fill="x")

        num_campos_por_columna = (len(self.datos_entrada) + 1) // 2
        etiquetas = list(self.datos_entrada.keys())

        for i, etiqueta in enumerate(etiquetas):
            row = i % num_campos_por_columna
            col = (i // num_campos_por_columna) * 2
            ttk.Label(entrada_frame, text=etiqueta).grid(row=row, column=col, sticky="e", padx=5, pady=2)

            if etiqueta == "Departamento":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly")
                combo['values'] = list(self.data.puestos_por_departamento.keys())
                combo.bind("<<ComboboxSelected>>", self._actualizar_puestos)
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Puesto":
                self.puesto_combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly")
                self.puesto_combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Género":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=["FEMENINO", "MASCULINO", "OTRO"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Turno":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=list(self.data.horarios_turno.keys()))
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Horario":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=["07:00 a 15:00", "15:00 a 23:00", "23:00 a 07:00"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Jornada":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=["LUNES A VIERNES", "LUNES, MIÉRCOLES, VIERNES", "MARTES Y JUEVES", "SÁBADOS Y DOMINGOS", "DOMINGOS", "SÁBADOS, DOMINGOS, DÍAS FECTIVOS", "MIÉRCOLES, JUEVES, VIERNES, SÁBADOS, DOMINGOS", "MARTES, JUEVES, SÁBADOS"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Tipo de Contratación":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=["BASIFICADOS", "HOMOLOGADOS", "REGULARIZADOS", "CONTRATO", "SUPLENTES O CUBREINCIDENCIAS", "OTRO"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            elif etiqueta == "Último Grado de Estudios":
                combo = ttk.Combobox(entrada_frame, textvariable=self.datos_entrada[etiqueta], state="readonly", values=["EDUCACIÓN BÁSICA", "EDUCACIÓN MEDIA SUPERIOR", "EDUCACIÓN SUPERIOR"])
                combo.grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
            else:
                ttk.Entry(entrada_frame, textvariable=self.datos_entrada[etiqueta]).grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")

        ttk.Button(entrada_frame, text="Registrar Trabajador", command=self._registrar_trabajador).grid(
            row=num_campos_por_columna+1, column=0, columnspan=4, pady=10)

        tabla_frame = self.create_labeled_frame(self.frame, "Historial de Trabajadores")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = etiquetas
        self.tabla_trabajadores, vscroll, hscroll = self.create_treeview_with_scroll(tabla_frame, columnas)
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.tabla_trabajadores.pack(fill="both", expand=True)

    def show(self):
        self.frame.pack(expand=True, fill="both")
        self._actualizar_tabla_historial()

    def _actualizar_puestos(self, *args):
        depto = self.datos_entrada["Departamento"].get()
        puestos = self.data.puestos_por_departamento.get(depto, [])
        self.puesto_combo['values'] = puestos
        self.datos_entrada["Puesto"].set('')

    def _validar_datos(self):
        for campo, var in self.datos_entrada.items():
            if not var.get().strip():
                messagebox.showwarning("Campo vacío", f"El campo '{campo}' es obligatorio.")
                return False
        return True

    def _registrar_trabajador(self):
        if not self._validar_datos():
            return

        jornada = self.datos_entrada["Jornada"].get()
        puesto = self.datos_entrada["Puesto"].get()
        clave = f"{puesto}_{jornada}"

        if self.data.cupo_jornada.get(clave, 0) >= 10:
            messagebox.showerror("Cupo lleno", "Esta jornada ha llegado al límite de trabajadores.")
            return

        registro = {k: v.get() for k, v in self.datos_entrada.items()}
        self.data.historial_trabajadores.append(registro)
        self.data.cupo_jornada[clave] = self.data.cupo_jornada.get(clave, 0) + 1

        nc = registro["Número de control"]
        if nc not in self.data.ids_control:
            self.data.ids_control.append(nc)
        self.data.datos_trabajadores[nc] = registro

        for var in self.datos_entrada.values():
            var.set('')
        if self.puesto_combo:
            self.puesto_combo['values'] = []
        self._actualizar_tabla_historial()
        self.app.asistencia_module.update_id_list()
        self.app.vacaciones_module.update_id_list()
        messagebox.showinfo("Éxito", "Trabajador registrado correctamente.")

    def _actualizar_tabla_historial(self):
        if self.tabla_trabajadores:
            self.tabla_trabajadores.delete(*self.tabla_trabajadores.get_children())
            for registro in self.data.historial_trabajadores:
                valores = [registro.get(col, "") for col in self.tabla_trabajadores["columns"]]
                self.tabla_trabajadores.insert('', 'end', values=valores)

# --- Clase Hijo 3: RegistroAsistenciaModule ---
class RegistroAsistenciaModule(BaseModule):
    def __init__(self, parent_frame, app_instance, data_store):
        super().__init__(parent_frame, app_instance, data_store)
        self.frame = tk.Frame(self.parent_frame)
        self.lista_ids_cb = None
        self.tabla_asistencia = None

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_departamento = tk.StringVar()
        self.var_puesto = tk.StringVar()
        self.var_turno = tk.StringVar()
        self.var_jornada = tk.StringVar()
        self.var_horario = tk.StringVar()
        self.var_estado = tk.StringVar()
        self.var_fecha = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.var_hora_entrada = tk.StringVar()
        self.var_hora_salida = tk.StringVar()
        self.var_horas_extra = tk.StringVar(value="0:00")

        self._create_widgets()

    def _create_widgets(self):
        form_frame = self.create_labeled_frame(self.frame, "Registro de Asistencia")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Número de Control:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.lista_ids_cb = ttk.Combobox(form_frame, textvariable=self.var_id, state="readonly", values=self.data.ids_control)
        self.lista_ids_cb.grid(row=0, column=1, padx=5, pady=5)
        self.lista_ids_cb.bind("<<ComboboxSelected>>", self._llenar_campos)

        campos_label = ["Nombre", "Departamento", "Puesto", "Turno", "Jornada", "Horario"]
        vars_campos = [self.var_nombre, self.var_departamento, self.var_puesto, self.var_turno, self.var_jornada, self.var_horario]

        for i, (lbl, varc) in enumerate(zip(campos_label, vars_campos)):
            ttk.Label(form_frame, text=lbl + ":").grid(row=i+1, column=0, padx=5, pady=2, sticky="e")
            ttk.Entry(form_frame, textvariable=varc, state="readonly").grid(row=i+1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Fecha:").grid(row=7, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=self.var_fecha, state="readonly").grid(row=7, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Hora Entrada:").grid(row=8, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=self.var_hora_entrada, state="readonly").grid(row=8, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Hora Salida:").grid(row=9, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=self.var_hora_salida, state="readonly").grid(row=9, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Horas Extra:").grid(row=10, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=self.var_horas_extra, state="readonly").grid(row=10, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(form_frame, text="Estado:").grid(row=11, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(form_frame, textvariable=self.var_estado, state="readonly").grid(row=11, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(form_frame, text="Registrar Entrada", command=self._registrar_entrada).grid(row=12, column=0, padx=10, pady=10)
        ttk.Button(form_frame, text="Registrar Salida", command=self._registrar_salida).grid(row=12, column=1, padx=10, pady=10)

        tabla_frame = self.create_labeled_frame(self.frame, "Historial de Asistencias")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                    "Jornada", "Horario", "Fecha", "Hora Entrada", "Hora Salida", "Estado", "Horas Extra")
        self.tabla_asistencia, vscroll, hscroll = self.create_treeview_with_scroll(tabla_frame, columnas)
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.tabla_asistencia.pack(fill="both", expand=True)

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.update_id_list()
        self._actualizar_tabla_asistencia()

    def _llenar_campos(self, event=None):
        nc = self.var_id.get()
        if nc in self.data.datos_trabajadores:
            t = self.data.datos_trabajadores[nc]
            self.var_nombre.set(t.get("Nombre", ""))
            self.var_departamento.set(t.get("Departamento", ""))
            self.var_puesto.set(t.get("Puesto", ""))
            self.var_turno.set(t.get("Turno", ""))
            self.var_jornada.set(t.get("Jornada", ""))
            self.var_horario.set(t.get("Horario", ""))
            self.var_estado.set("")
            self.var_hora_entrada.set("")
            self.var_hora_salida.set("")
            self.var_horas_extra.set("0:00")
        else:
            self.var_nombre.set("")
            self.var_departamento.set("")
            self.var_puesto.set("")
            self.var_turno.set("")
            self.var_jornada.set("")
            self.var_horario.set("")
            self.var_estado.set("")
            self.var_hora_entrada.set("")
            self.var_hora_salida.set("")
            self.var_horas_extra.set("0:00")

    def _calcular_estado_entrada(self, hora_entrada_str, turno):
        fmt = "%H:%M"
        try:
            hora_entrada = datetime.strptime(hora_entrada_str, fmt)
        except ValueError:
            messagebox.showerror("Error de formato", "Hora de entrada no válida.")
            return "Desconocido"

        inicio_str, fin_str = self.data.horarios_turno.get(turno, ("07:00", "15:00"))
        try:
            inicio = datetime.strptime(inicio_str, fmt)
        except ValueError:
            messagebox.showerror("Error de formato", "Horario de turno no válido.")
            return "Desconocido"

        if turno == "TURNO NOCTURNO":
            if hora_entrada.hour < inicio.hour:
                hora_entrada += timedelta(days=1)
            if inicio.hour >= 12 and hora_entrada.hour < 12:
                 inicio -= timedelta(days=1)

        delta_minutos = (hora_entrada - inicio).total_seconds() / 60

        if -5 <= delta_minutos <= 5:
            return "Asistencia"
        elif 5 < delta_minutos <= 30:
            return "Retardo menor"
        elif delta_minutos > 30:
            return "Retardo mayor"
        else:
            return "Asistencia"

    def _actualizar_contador_retardos(self, nc, estado):
        if nc not in self.data.contador_retardos:
            self.data.contador_retardos[nc] = {"retardo_menor": 0, "retardo_mayor": 0, "faltas": 0}

        if estado == "Retardo menor":
            self.data.contador_retardos[nc]["retardo_menor"] += 1
            if self.data.contador_retardos[nc]["retardo_menor"] >= 3:
                self.data.contador_retardos[nc]["faltas"] += 1
                self.data.contador_retardos[nc]["retardo_menor"] = 0
                messagebox.showinfo("Falta asignada",
                                    f"Al trabajador {nc} se le asignó 1 falta por 3 retardos menores. Total faltas: {self.data.contador_retardos[nc]['faltas']}")
        elif estado == "Retardo mayor":
            self.data.contador_retardos[nc]["retardo_mayor"] += 1
            if self.data.contador_retardos[nc]["retardo_mayor"] >= 2:
                self.data.contador_retardos[nc]["faltas"] += 1
                self.data.contador_retardos[nc]["retardo_mayor"] = 0
                messagebox.showinfo("Falta asignada",
                                    f"Al trabajador {nc} se le asignó 1 falta por 2 retardos mayores. Total faltas: {self.data.contador_retardos[nc]['faltas']}")

    def _registrar_entrada(self):
        nc = self.var_id.get()
        if not nc or nc not in self.data.datos_trabajadores:
            messagebox.showerror("Error", "Seleccione un número de control válido.")
            return

        ahora = datetime.now()
        hora_entrada_str = ahora.strftime("%H:%M")
        fecha_actual = ahora.strftime("%Y-%m-%d")

        for registro in self.data.asistencia_registros:
            if registro[0] == nc and registro[7] == fecha_actual and registro[8]:
                messagebox.showwarning("Advertencia", "Ya se registró una entrada para este trabajador hoy.")
                return

        turno = self.var_turno.get()
        if not turno or turno not in self.data.horarios_turno:
            messagebox.showerror("Error", "El trabajador no tiene un turno válido asignado.")
            return

        estado = self._calcular_estado_entrada(hora_entrada_str, turno)
        self.var_hora_entrada.set(hora_entrada_str)
        self.var_estado.set(estado)

        self._actualizar_contador_retardos(nc, estado)

        messagebox.showinfo("Entrada registrada", f"Entrada registrada a las {hora_entrada_str} con estado: {estado}")

    def _registrar_salida(self):
        nc = self.var_id.get()
        if not nc or nc not in self.data.datos_trabajadores:
            messagebox.showerror("Error", "Seleccione un número de control válido.")
            return
        if not self.var_hora_entrada.get():
            messagebox.showwarning("Error", "Primero debe registrar la entrada.")
            return

        ahora = datetime.now()
        hora_salida_str = ahora.strftime("%H:%M")
        self.var_hora_salida.set(hora_salida_str)

        turno = self.var_turno.get()
        if not turno or turno not in self.data.horarios_turno:
            messagebox.showerror("Error", "El trabajador no tiene un turno válido asignado para calcular horas extra.")
            return

        hora_ini_str, hora_fin_str = self.data.horarios_turno.get(turno)

        fmt = "%H:%M"
        try:
            entrada_dt = datetime.strptime(self.var_hora_entrada.get(), fmt)
            salida_dt = datetime.strptime(hora_salida_str, fmt)
            fin_dt = datetime.strptime(hora_fin_str, fmt)
        except ValueError:
            messagebox.showerror("Error de formato", "Problema al parsear las horas.")
            return

        if turno == "TURNO NOCTURNO":
            if salida_dt < entrada_dt:
                salida_dt += timedelta(days=1)
            if fin_dt < entrada_dt:
                fin_dt += timedelta(days=1)
            if fin_dt < entrada_dt and entrada_dt.hour >= 12 and fin_dt.hour < 12:
                fin_dt += timedelta(days=1)
            if fin_dt > salida_dt and salida_dt.hour < 12 and fin_dt.hour >= 12:
                fin_dt -= timedelta(days=1)

        extra = salida_dt - fin_dt
        horas_extra = "0:00"
        if extra.total_seconds() > 0:
            total_minutos = int(extra.total_seconds() // 60)
            horas = total_minutos // 60
            minutos = total_minutos % 60
            horas_extra = f"{horas}:{minutos:02d}"
        self.var_horas_extra.set(horas_extra)

        actualizado = False
        fecha_actual_str = self.var_fecha.get()
        hora_entrada_prevista = self.var_hora_entrada.get()

        for i, reg in enumerate(self.data.asistencia_registros):
            if reg[0] == nc and reg[7] == fecha_actual_str and reg[8] == hora_entrada_prevista:
                self.data.asistencia_registros[i] = (
                    nc,
                    self.var_nombre.get(),
                    self.var_departamento.get(),
                    self.var_puesto.get(),
                    self.var_turno.get(),
                    self.var_jornada.get(),
                    self.var_horario.get(),
                    fecha_actual_str,
                    self.var_hora_entrada.get(),
                    self.var_hora_salida.get(),
                    self.var_estado.get(),
                    horas_extra
                )
                actualizado = True
                break

        if not actualizado:
             fila = (
                nc,
                self.var_nombre.get(),
                self.var_departamento.get(),
                self.var_puesto.get(),
                self.var_turno.get(),
                self.var_jornada.get(),
                self.var_horario.get(),
                fecha_actual_str,
                self.var_hora_entrada.get(),
                self.var_hora_salida.get(),
                self.var_estado.get(),
                horas_extra
            )
             self.data.asistencia_registros.append(fila)

        self._actualizar_tabla_asistencia()
        messagebox.showinfo("Salida registrada", f"Salida registrada a las {hora_salida_str}. Horas extra: {horas_extra}")

        self.var_id.set("")
        self.var_nombre.set("")
        self.var_departamento.set("")
        self.var_puesto.set("")
        self.var_turno.set("")
        self.var_jornada.set("")
        self.var_horario.set("")
        self.var_estado.set("")
        self.var_hora_entrada.set("")
        self.var_hora_salida.set("")
        self.var_horas_extra.set("0:00")
        self.update_id_list()

    def _actualizar_tabla_asistencia(self):
        if self.tabla_asistencia:
            self.tabla_asistencia.delete(*self.tabla_asistencia.get_children())
            for registro in self.data.asistencia_registros:
                self.tabla_asistencia.insert('', 'end', values=registro)

    def update_id_list(self):
        self.lista_ids_cb['values'] = self.data.ids_control
        if self.data.ids_control:
            self.lista_ids_cb.set(self.data.ids_control[0])
            self._llenar_campos()

# --- Clase Hijo 4: RegistroVacacionesModule ---
class RegistroVacacionesModule(BaseModule):
    def __init__(self, parent_frame, app_instance, data_store):
        super().__init__(parent_frame, app_instance, data_store)
        self.frame = tk.Frame(self.parent_frame)

        self.entry_nc = None
        self.entradas_autocompletar = {}
        self.division_cb = None
        self.quincena_cb = None
        self.dias_eco_cb = None
        self.periodo_cb = None
        self.tree_vac = None
        self.tree_eco = None
        self.tree_pe = None

        self._create_widgets()

    def _create_widgets(self):
        canvas = tk.Canvas(self.frame)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text="Registro de Vacaciones", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(scroll_frame, text="Número de Control:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_nc = ttk.Combobox(scroll_frame, state="readonly", values=self.data.ids_control)
        self.entry_nc.grid(row=1, column=1, pady=5, sticky="ew")
        self.entry_nc.bind("<<ComboboxSelected>>", self._autocompletar)

        campos = ["Nombre", "Departamento", "Puesto", "Turno", "Jornada", "Horario"]
        for i, campo in enumerate(campos):
            tk.Label(scroll_frame, text=campo + ":").grid(row=i+2, column=0, sticky="e", padx=5, pady=3)
            ent = tk.Entry(scroll_frame, state="readonly")
            ent.grid(row=i+2, column=1, pady=3, sticky="ew")
            self.entradas_autocompletar[campo] = ent

        tk.Label(scroll_frame, text="División:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.division_cb = ttk.Combobox(scroll_frame, state="readonly", values=["Primavera", "Invierno"])
        self.division_cb.grid(row=8, column=1, sticky="ew", pady=5)
        self.division_cb.bind("<<ComboboxSelected>>", self._actualizar_quincenas)

        tk.Label(scroll_frame, text="Quincena:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
        self.quincena_cb = ttk.Combobox(scroll_frame, state="readonly")
        self.quincena_cb.grid(row=9, column=1, sticky="ew", pady=5)

        tk.Label(scroll_frame, text="Días Económicos (máximo 8 días/año):").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.dias_eco_cb = ttk.Combobox(scroll_frame, state="readonly", values=["SI", "NO"])
        self.dias_eco_cb.grid(row=10, column=1, sticky="ew", pady=5)

        tk.Label(scroll_frame, text="Período Extraordinario:").grid(row=11, column=0, sticky="e", padx=5, pady=5)
        self.periodo_cb = ttk.Combobox(scroll_frame, state="readonly", values=[
            "Alto Riesgo (15 días)", "Mediano Riesgo (8 días)", "Bajo Riesgo (3 días)"])
        self.periodo_cb.grid(row=11, column=1, sticky="ew", pady=5)

        ttk.Button(scroll_frame, text="Registrar", command=self._registrar_vacaciones).grid(row=12, column=0, columnspan=3, pady=15)

        tk.Label(scroll_frame, text="Historial Vacaciones").grid(row=13, column=0, columnspan=4, pady=5)
        columns_vac = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                       "Jornada", "Horario", "División", "Quincena")
        self.tree_vac, vscroll_vac, hscroll_vac = self.create_treeview_with_scroll(scroll_frame, columns_vac, heights=7)
        self.tree_vac.grid(row=14, column=0, columnspan=4, pady=5, sticky="ew")
        vscroll_vac.grid(row=14, column=4, sticky="ns")
        hscroll_vac.grid(row=15, column=0, columnspan=4, sticky="ew")
        self.tree_vac.configure(yscrollcommand=vscroll_vac.set, xscrollcommand=hscroll_vac.set)

        tk.Label(scroll_frame, text="Historial Días Económicos").grid(row=16, column=0, columnspan=4, pady=5)
        columns_eco = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                       "Jornada", "Horario", "Fecha", "Días Económicos Registrados")
        self.tree_eco, vscroll_eco, hscroll_eco = self.create_treeview_with_scroll(scroll_frame, columns_eco, heights=5)
        self.tree_eco.grid(row=17, column=0, columnspan=4, pady=5, sticky="ew")
        vscroll_eco.grid(row=17, column=4, sticky="ns")
        hscroll_eco.grid(row=18, column=0, columnspan=4, sticky="ew")
        self.tree_eco.configure(yscrollcommand=vscroll_eco.set, xscrollcommand=hscroll_eco.set)

        tk.Label(scroll_frame, text="Historial Períodos Extraordinarios").grid(row=19, column=0, columnspan=4, pady=5)
        columns_pe = ("Número de Control", "Nombre", "Departamento", "Puesto", "Turno",
                      "Jornada", "Horario", "Nivel de Riesgo", "Días", "Fecha Registro")
        self.tree_pe, vscroll_pe, hscroll_pe = self.create_treeview_with_scroll(scroll_frame, columns_pe, heights=5)
        self.tree_pe.grid(row=20, column=0, columnspan=4, pady=5, sticky="ew")
        vscroll_pe.grid(row=20, column=4, sticky="ns")
        hscroll_pe.grid(row=21, column=0, columnspan=4, sticky="ew")
        self.tree_pe.configure(yscrollcommand=vscroll_pe.set, xscrollcommand=hscroll_pe.set)

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.update_id_list()
        self._actualizar_tablas_vacaciones()

    def _autocompletar(self, event=None):
        nc = self.entry_nc.get()
        if nc in self.data.datos_trabajadores:
            trabajador = self.data.datos_trabajadores[nc]
            for campo, ent in self.entradas_autocompletar.items():
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.insert(0, trabajador.get(campo, ""))
                ent.config(state="readonly")
        else:
            messagebox.showerror("Error", "Número de control no encontrado.")
            for ent in self.entradas_autocompletar.values():
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.config(state="readonly")

    def _actualizar_quincenas(self, event=None):
        quincenas_primavera = [
            "1-15 Enero", "16-31 Enero", "1-15 Febrero", "16-28 Febrero",
            "1-15 Marzo", "16-31 Marzo", "1-15 Abril", "16-30 Abril",
            "1-15 Mayo", "16-31 Mayo", "1-15 Junio", "16-30 Junio"
        ]
        quincenas_invierno = [
            "1-15 Julio", "16-31 Julio", "1-15 Agosto", "16-31 Agosto",
            "1-15 Septiembre", "16-30 Septiembre", "1-15 Octubre", "16-31 Octubre",
            "1-15 Noviembre", "16-30 Noviembre", "1-15 Diciembre", "16-31 Diciembre"
        ]
        if self.division_cb.get() == "Primavera":
            self.quincena_cb['values'] = quincenas_primavera
        elif self.division_cb.get() == "Invierno":
            self.quincena_cb['values'] = quincenas_invierno
        self.quincena_cb.set('')

    def _contar_dias_eco(self, nc):
        year_actual = str(datetime.now().year)
        count = 0
        for d in self.data.dias_economicos_registros:
            if d["Número de Control"] == nc and d["Fecha"].startswith(year_actual):
                count += 1
        return count

    def _registrar_vacaciones(self):
        nc = self.entry_nc.get()
        if not nc or nc not in self.data.datos_trabajadores:
            messagebox.showerror("Error", "Seleccione un número de control válido.")
            return

        division = self.division_cb.get()
        quincena = self.quincena_cb.get()
        if division == "" or quincena == "":
            messagebox.showwarning("Aviso", "Seleccione división y quincena para registrar vacaciones.")
            return

        trabajador = self.data.datos_trabajadores[nc]
        jornada = trabajador.get("Jornada", "")
        puesto = trabajador.get("Puesto", "")
        horario = trabajador.get("Horario", "")

        count = sum(1 for r in self.data.vacaciones_registros if
                    r["División"] == division and r["Quincena"] == quincena and
                    r["Jornada"] == jornada and r["Puesto"] == puesto and
                    r["Horario"] == horario)

        if count >= 3:
            messagebox.showwarning("Cupo lleno", "Esta quincena ya alcanzó el límite de 3 trabajadores para esta jornada, puesto y horario.")
            return

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
        self.data.vacaciones_registros.append(registro_vac)

        if self.dias_eco_cb.get() == "SI":
            dias_anteriores = self._contar_dias_eco(nc)
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
                self.data.dias_economicos_registros.append(registro_eco)

        pe = self.periodo_cb.get()
        if pe != "":
            dias_pe = 0
            if "Alto" in pe: dias_pe = 15
            elif "Mediano" in pe: dias_pe = 8
            elif "Bajo" in pe: dias_pe = 3

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
            self.data.periodo_extraordinario_registros.append(registro_pe)

        messagebox.showinfo("Registrado", "Vacaciones y/o submódulos registrados correctamente.")
        self._actualizar_tablas_vacaciones()
        self._limpiar_campos()

    def _limpiar_campos(self):
        self.entry_nc.set("")
        for ent in self.entradas_autocompletar.values():
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.config(state="readonly")
        self.division_cb.set('')
        self.quincena_cb.set('')
        self.dias_eco_cb.set('')
        self.periodo_cb.set('')

    def _actualizar_tablas_vacaciones(self):
        self.tree_vac.delete(*self.tree_vac.get_children())
        for registro in self.data.vacaciones_registros:
            self.tree_vac.insert('', 'end', values=tuple(registro.values()))

        self.tree_eco.delete(*self.tree_eco.get_children())
        for registro in self.data.dias_economicos_registros:
            self.tree_eco.insert('', 'end', values=tuple(registro.values()))

        self.tree_pe.delete(*self.tree_pe.get_children())
        for registro in self.data.periodo_extraordinario_registros:
            self.tree_pe.insert('', 'end', values=tuple(registro.values()))

    def update_id_list(self):
        self.entry_nc['values'] = self.data.ids_control
        if self.data.ids_control:
            self.entry_nc.set(self.data.ids_control[0])
            self._autocompletar()

# --- Clase Principal de la Aplicación: HospitalApp ---
class HospitalApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema Hospitalario")
        self.ventana.geometry("1200x800")

        self.data_store = HospitalData()

        self.menu_lateral = tk.Frame(self.ventana, width=200, bg="#2c3e50")
        self.menu_lateral.pack(side="left", fill="y")

        self.contenido_dinamico = tk.Frame(self.ventana)
        self.contenido_dinamico.pack(side="right", fill="both", expand=True)

        self.bienvenida_module = BienvenidaModule(self.contenido_dinamico, self, self.data_store)
        self.trabajadores_module = RegistroTrabajadoresModule(self.contenido_dinamico, self, self.data_store)
        self.asistencia_module = RegistroAsistenciaModule(self.contenido_dinamico, self, self.data_store)
        self.vacaciones_module = RegistroVacacionesModule(self.contenido_dinamico, self, self.data_store)

        self._crear_botones_menu()
        self._cargar_bienvenida()

    def _ocultar_frames(self):
        for frame in self.contenido_dinamico.winfo_children():
            frame.pack_forget()

    def _cargar_bienvenida(self):
        self._ocultar_frames()
        self.bienvenida_module.show()

    def _cargar_registro_trabajadores(self):
        self._ocultar_frames()
        self.trabajadores_module.show()

    def _cargar_registro_asistencia(self):
        self._ocultar_frames()
        self.asistencia_module.show()

    def _cargar_registro_vacaciones(self):
        self._ocultar_frames()
        self.vacaciones_module.show()

    def _crear_botones_menu(self):
        btn_bienvenida = tk.Button(self.menu_lateral, text="Bienvenida", bg='#34495e', fg="white", command=self._cargar_bienvenida)
        btn_bienvenida.pack(fill="x", pady=5)

        btn_registro_trab = tk.Button(self.menu_lateral, text="Registro Trabajadores", bg='#34495e', fg="white", command=self._cargar_registro_trabajadores)
        btn_registro_trab.pack(fill="x", pady=5)

        btn_registro_asistencia = tk.Button(self.menu_lateral, text="Registro Asistencia", bg='#34495e', fg="white", command=self._cargar_registro_asistencia)
        btn_registro_asistencia.pack(fill="x", pady=5)

        btn_registro_vacaciones = tk.Button(self.menu_lateral, text="Registro Vacaciones", bg='#34495e', fg="white", command=self._cargar_registro_vacaciones)
        btn_registro_vacaciones.pack(fill="x", pady=5)

        btn_salir = tk.Button(self.menu_lateral, text="Salir", bg='#34495e', fg="white", command=self.ventana.quit)
        btn_salir.pack(fill="x", pady=5)

    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = HospitalApp()
    app.run()
