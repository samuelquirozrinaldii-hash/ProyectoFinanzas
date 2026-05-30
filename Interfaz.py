import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from Conexion import crear_tabla
import Funciones as crud

class AppFinanzas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Finanzas Personales")
        self.geometry("850x550")
        self.configure(bg="#f0f2f5")
        
        # Asegurar que la tabla exista al iniciar
        crear_tabla()
        
        self.crear_componentes()
        self.cargar_datos()

    def crear_componentes(self):
        # --- TÍTULO PRINCIPAL ---
        lbl_titulo = tk.Label(self, text="GESTOR DE FINANZAS PERSONALES", font=("Arial", 16, "bold"), bg="#1877f2", fg="white", pady=10)
        lbl_titulo.pack(fill=tk.X)

        # --- CONTENEDOR IZQUIERDO: FORMULARIO ---
        frame_form = tk.LabelFrame(self, text=" Nueva Transacción / Edición ", font=("Arial", 10, "bold"), bg="#f0f2f5", padx=15, pady=15)
        frame_form.place(x=20, y=70, width=320, height=320)

        tk.Label(frame_form, text="Tipo:", bg="#f0f2f5", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.cmb_tipo = ttk.Combobox(frame_form, values=["Ingreso", "Gasto"], state="readonly")
        self.cmb_tipo.grid(row=0, column=1, pady=5, sticky="we")
        self.cmb_tipo.set("Ingreso")

        tk.Label(frame_form, text="Monto ($):", bg="#f0f2f5", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_monto = ttk.Entry(frame_form)
        self.txt_monto.grid(row=1, column=1, pady=5, sticky="we")

        tk.Label(frame_form, text="Categoría:", bg="#f0f2f5", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.txt_categoria = ttk.Entry(frame_form)
        self.txt_categoria.grid(row=2, column=1, pady=5, sticky="we")

        tk.Label(frame_form, text="Descripción:", bg="#f0f2f5", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.txt_descripcion = ttk.Entry(frame_form)
        self.txt_descripcion.grid(row=3, column=1, pady=5, sticky="we")

        # ID oculto o visible para saber si estamos editando
        tk.Label(frame_form, text="ID Seleccionado:", bg="#f0f2f5", fg="gray").grid(row=4, column=0, sticky="w", pady=5)
        self.lbl_id = tk.Label(frame_form, text="Ninguno", bg="#f0f2f5", fg="blue", font=("Arial", 9, "bold"))
        self.lbl_id.grid(row=4, column=1, sticky="w", pady=5)

        # Botones del Formulario
        btn_guardar = tk.Button(frame_form, text="Guardar Registro", bg="#42b72a", fg="white", font=("Arial", 10, "bold"), command=self.guardar_datos)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")
        
        btn_limpiar = tk.Button(frame_form, text="Limpiar Campos", bg="#606770", fg="white", command=self.limpiar_campos)
        btn_limpiar.grid(row=6, column=0, columnspan=2, sticky="we")

        # --- CONTENEDOR DERECHO: TABLA DE HISTORIAL ---
        frame_tabla = tk.LabelFrame(self, text=" Historial de Transacciones ", font=("Arial", 10, "bold"), bg="#f0f2f5", padx=10, pady=10)
        frame_tabla.place(x=360, y=70, width=470, height=320)

        # Configuración de columnas de la tabla (Treeview)
        columnas = ("id", "tipo", "monto", "categoria", "fecha", "descripcion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        self.tabla.heading("id", text="ID")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("monto", text="Monto")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("descripcion", text="Descripción")

        self.tabla.column("id", width=30, anchor="center")
        self.tabla.column("tipo", width=60, anchor="center")
        self.tabla.column("monto", width=70, anchor="e")
        self.tabla.column("categoria", width=80, anchor="w")
        self.tabla.column("fecha", width=85, anchor="center")
        self.tabla.column("descripcion", width=120, anchor="w")
        
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.cargar_item_seleccionado)

        # --- CONTENEDOR INFERIOR: BALANCE Y ACCIONES ---
        self.frame_balance = tk.Frame(self, bg="#e4e6eb", bd=1, relief=tk.SOLID)
        self.frame_balance.place(x=20, y=410, width=320, height=110)
        
        self.lbl_ingresos = tk.Label(self.frame_balance, text="Ingresos: $0.00", fg="green", bg="#e4e6eb", font=("Arial", 10, "bold"))
        self.lbl_ingresos.pack(pady=2)
        self.lbl_gastos = tk.Label(self.frame_balance, text="Gastos: $0.00", fg="red", bg="#e4e6eb", font=("Arial", 10, "bold"))
        self.lbl_gastos.pack(pady=2)
        self.lbl_neto = tk.Label(self.frame_balance, text="Balance Neto: $0.00", fg="black", bg="#e4e6eb", font=("Arial", 11, "bold"))
        self.lbl_neto.pack(pady=5)

        # Botones de Acción sobre la Tabla
        btn_eliminar = tk.Button(self, text="Eliminar Seleccionado", bg="#f02849", fg="white", font=("Arial", 10, "bold"), command=self.eliminar_datos)
        btn_eliminar.place(x=360, y=410, width=220, height=40)

        btn_salir = tk.Button(self, text="Salir del Gestor", bg="#606770", fg="white", font=("Arial", 10, "bold"), command=self.destroy)
        btn_salir.place(x=610, y=410, width=220, height=40)

    # --- LÓGICA DE LA INTERFAZ ---

    def cargar_datos(self):
        # Limpiar la tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Insertar registros actualizados desde la Base de Datos
        transacciones = crud.ver_transacciones()
        for t in transacciones:
            # Formatear el monto con el signo de dólar para la vista
            monto_formateado = f"${t[2]:.2f}"
            self.tabla.insert("", tk.END, values=(t[0], t[1], monto_formateado, t[3], t[4], t[5]))
            
        # Actualizar los cuadros de Balance General
        ingresos, gastos, balance = crud.obtener_balance()
        self.lbl_ingresos.config(text=f"Total Ingresos: ${ingresos:.2f}")
        self.lbl_gastos.config(text=f"Total Gastos: ${gastos:.2f}")
        self.lbl_neto.config(text=f"Balance Neto: ${balance:.2f}")
        
        if balance < 0:
            self.lbl_neto.config(fg="red")
        else:
            self.lbl_neto.config(fg="green")

    def guardar_datos(self):
        try:
            tipo = self.cmb_tipo.get()
            monto = float(self.txt_monto.get())
            categoria = self.txt_categoria.get().strip().capitalize()
            descripcion = self.txt_descripcion.get().strip()
            fecha_hoy = date.today().strftime("%Y-%m-%d")

            if not categoria:
                messagebox.showwarning("Atención", "La categoría no puede estar vacía.")
                return

            id_actual = self.lbl_id.cget("text")

            if id_actual == "Ninguno":
                # Si no hay ID seleccionado, es una NUEVA transacción
                crud.registrar_transaccion(tipo, monto, categoria, fecha_hoy, descripcion)
                messagebox.showinfo("Éxito", "Transacción registrada correctamente.")
            else:
                # Si hay un ID en pantalla, se EDITA el registro existente
                crud.actualizar_transaccion(int(id_actual), monto, categoria)
                messagebox.showinfo("Éxito", f"Registro {id_actual} modificado con éxito.")

            self.limpiar_campos()
            self.cargar_datos()

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un monto numérico válido.")

    def cargar_item_seleccionado(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item['values']
            
            # Pasar los datos de la fila de vuelta a los inputs para poder editarlos
            self.lbl_id.config(text=valores[0])
            self.cmb_tipo.set(valores[1])
            # Quitar el signo de '$' para poder convertirlo a float
            self.txt_monto.delete(0, tk.END)
            self.txt_monto.insert(0, valores[2].replace('$', ''))
            self.txt_categoria.delete(0, tk.END)
            self.txt_categoria.insert(0, valores[3])
            self.txt_descripcion.delete(0, tk.END)
            self.txt_descripcion.insert(0, valores[5])

    def eliminar_datos(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una transacción de la tabla para eliminar.")
            return

        valores = self.tabla.item(seleccion[0])['values']
        id_reg = valores[0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar el registro con ID {id_reg}?")
        if confirmar:
            crud.eliminar_transaccion(id_reg)
            self.limpiar_campos()
            self.cargar_datos()

    def limpiar_campos(self):
        self.lbl_id.config(text="Ninguno")
        self.cmb_tipo.set("Ingreso")
        self.txt_monto.delete(0, tk.END)
        self.txt_categoria.delete(0, tk.END)
        self.txt_descripcion.delete(0, tk.END)

if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()
