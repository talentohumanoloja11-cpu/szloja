import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

ARCHIVO_DATOS = "Base_Datos_Personal_Corregida.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        messagebox.showerror("Error", "No se encontró el archivo base.")
        return None
    try:
        df = pd.read_csv(ARCHIVO_DATOS, sep=';', encoding='latin-1')
        df.columns = df.columns.str.strip().str.upper()
        if 'CEDULA' in df.columns:
            df['CEDULA'] = df['CEDULA'].astype(str).str.replace('.0', '', regex=False).str.zfill(10)
            return df
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Fallo al cargar: {e}")
        return None

def buscar_servidor():
    df = cargar_datos()
    if df is not None:
        id_buscado = entry_id.get().strip().zfill(10)
        resultado = df[df['CEDULA'] == id_buscado]
        
        if not resultado.empty:
            registro = resultado.iloc[-1]
            # Habilitar campos para edición
            entry_nombre.config(state="normal")
            entry_grado.config(state="normal")
            var_nombre.set(registro['APELLIDOS Y NOMBRES'])
            var_grado.set(registro['GRADO'])
            lbl_status.config(text="✅ Datos cargados. Puede editar y guardar.", fg="green")
        else:
            messagebox.showinfo("Búsqueda", "Cédula no encontrada.")

def guardar_actualizacion():
    cedula_act = entry_id.get().strip().zfill(10)
    nuevo_nombre = var_nombre.get().strip().upper()
    nuevo_grado = var_grado.get().strip().upper()
    
    if not cedula_act or not nuevo_nombre:
        messagebox.showwarning("Aviso", "Busque un registro antes de guardar.")
        return

    try:
        df = pd.read_csv(ARCHIVO_DATOS, sep=';', encoding='latin-1')
        df.columns = df.columns.str.strip().str.upper()
        df['CEDULA'] = df['CEDULA'].astype(str).str.replace('.0', '', regex=False).str.zfill(10)

        # Actualizar todas las filas que coincidan con esa cédula
        if cedula_act in df['CEDULA'].values:
            df.loc[df['CEDULA'] == cedula_act, 'APELLIDOS Y NOMBRES'] = nuevo_nombre
            df.loc[df['CEDULA'] == cedula_act, 'GRADO'] = nuevo_grado
            
            # Guardar respetando el formato original de Excel
            df.to_csv(ARCHIVO_DATOS, index=False, sep=';', encoding='latin-1')
            messagebox.showinfo("Éxito", "Información actualizada correctamente.")
            limpiar_pantalla()
        else:
            messagebox.showerror("Error", "No se pudo reubicar el registro para guardar.")
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def limpiar_pantalla():
    entry_id.delete(0, tk.END)
    var_nombre.set("")
    var_grado.set("")
    entry_nombre.config(state="readonly")
    entry_grado.config(state="readonly")
    lbl_status.config(text="Esperando nueva consulta...", fg="black")

# --- Interfaz ---
app = tk.Tk()
app.title("Talento Humano - SZ LOJA")
app.geometry("550x450")

tk.Label(app, text="ACTUALIZACIÓN DE DATOS DEL PERSONAL", font=("Arial", 12, "bold")).pack(pady=20)

frame_b = tk.Frame(app)
frame_b.pack(pady=10)
entry_id = tk.Entry(frame_b, font=("Arial", 12), width=15, justify="center")
entry_id.pack(side="left", padx=5)
tk.Button(frame_b, text="🔍 BUSCAR", command=buscar_servidor, bg="#0d47a1", fg="white").pack(side="left")

# Campos editables
tk.Label(app, text="Apellidos y Nombres:").pack(pady=(20,0))
var_nombre = tk.StringVar()
entry_nombre = tk.Entry(app, textvariable=var_nombre, font=("Arial", 10), width=60, state="readonly")
entry_nombre.pack(pady=5)

tk.Label(app, text="Grado:").pack(pady=(10,0))
var_grado = tk.StringVar()
entry_grado = tk.Entry(app, textvariable=var_grado, font=("Arial", 10), width=60, state="readonly")
entry_grado.pack(pady=5)

lbl_status = tk.Label(app, text="Ingrese cédula para comenzar")
lbl_status.pack(pady=10)

# Botones de acción
btn_save = tk.Button(app, text="💾 GUARDAR CAMBIOS", command=guardar_actualizacion, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"), width=25)
btn_save.pack(pady=10)

tk.Button(app, text="🧹 Limpiar", command=limpiar_pantalla).pack()

app.mainloop()