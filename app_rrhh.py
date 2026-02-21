import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="RR.HH. SZ-LOJA", layout="centered")

ARCHIVO_DATOS = "Base_Datos_Personal_Corregida.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        df = pd.read_csv(ARCHIVO_DATOS, sep=';', encoding='latin-1')
        df.columns = df.columns.str.strip().str.upper()
        if 'CEDULA' in df.columns:
            df['CEDULA'] = df['CEDULA'].astype(str).str.replace('.0', '', regex=False).str.zfill(10)
            return df
    return None

st.title("🛡️ Gestión de Personal - Subzona Loja")
st.subheader("Actualización de Datos en Línea")

df = cargar_datos()

if df is not None:
    # Buscador en la barra lateral o principal
    cedula_buscar = st.text_input("Ingrese Cédula del Servidor Policial:", max_chars=10)
    
    if cedula_buscar:
        cedula_buscar = cedula_buscar.zfill(10)
        resultado = df[df['CEDULA'] == cedula_buscar]
        
        if not resultado.empty:
            registro = resultado.iloc[-1]
            st.success("Personal Localizado")
            
            # Formulario de edición
            with st.form("form_edicion"):
                nuevo_nombre = st.text_input("Apellidos y Nombres:", value=registro['APELLIDOS Y NOMBRES'])
                nuevo_grado = st.text_input("Grado Actual:", value=registro['GRADO'])
                
                if st.form_submit_button("💾 Guardar Cambios"):
                    # Actualizar el DataFrame
                    df.loc[df['CEDULA'] == cedula_buscar, 'APELLIDOS Y NOMBRES'] = nuevo_nombre.upper()
                    df.loc[df['CEDULA'] == cedula_buscar, 'GRADO'] = nuevo_grado.upper()
                    
                    # Guardar en el archivo
                    df.to_csv(ARCHIVO_DATOS, index=False, sep=';', encoding='latin-1')
                    st.balloons()
                    st.success(f"¡Datos de {nuevo_nombre} actualizados!")
        else:
            st.error("La cédula no consta en los registros.")
else:
    st.warning("No se encontró la base de datos CSV.")
