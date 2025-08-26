import pandas as pd
import streamlit as st
from datetime import datetime

# Archivo de trabajo
archivo_excel = 'boletines.xlsx'

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_excel(archivo_excel)

df = cargar_datos()

# Quita espacios en blanco
df.columns = df.columns.str.strip()  

# Elimina tildes
df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')  

st.write("🧩 Columnas actuales:", df.columns.tolist())

# Asegurar que las fechas están en formato datetime
df['Recordatorio'] = pd.to_datetime(df['Recordatorio'], dayfirst=True, errors='coerce')
df['Fecha de entrega'] = pd.to_datetime(df['Fecha de entrega'], dayfirst=True, errors='coerce')
df['Fecha de publicacion'] = pd.to_datetime(df['Fecha de publicacion'], dayfirst=True, errors='coerce')

# Agregar columna "Estado" si no existe
if 'Estado' not in df.columns:
    df['Estado'] = 'Pendiente'

st.set_page_config(page_title="Gestión de Boletines", layout="wide")
st.title("🗞️ Panel de Gestión de Boletines")

hoy = pd.to_datetime(datetime.today().date())

# Alertas importantes
st.subheader("🔔 Alertas del día")

hoy = pd.Timestamp(date.today())

# Filtrar filas donde la fecha de recordatorio sea hoy (ignora horas y errores)
alertas_hoy = df[
    pd.to_datetime(df['Recordatorio'], errors='coerce').dt.normalize() == hoy.normalize()
]

if not alertas_hoy.empty:
    for i, row in alertas_hoy.iterrows():
        try:
            st.warning(f"📧 Recordatorio para *{row['Responsable']}* - **{row['Tema/Materia']}** ({row['Tipo de Boletin']})")
            st.markdown(f"🗓️ Fecha de entrega: **{row['Fecha de entrega'].date() if pd.notnull(row['Fecha de entrega']) else '—'}**")
        except KeyError as e:
            st.warning(f"⚠️ Faltan columnas en esta fila: {e}")
else:
    st.success("✅ No hay alertas por hoy. Todo en orden.")

# Mostrar y editar cada trabajo
st.subheader("📋 Lista de trabajos")
for i, row in df.iterrows():
    try:
        with st.expander(f"📌 {row['Tema/Materia']} | {row['Tipo de Boletin']} | {row['Responsable']}"):
            st.markdown(f"**Instancia/Oficina:** {row['instancia/oficina']}")
            st.markdown(f"**Numero de boletin:** {row['numero boletin']}")
            st.markdown(f"**Recordatorio:** {row['Recordatorio'].date() if pd.notnull(row['Recordatorio']) else '—'}")
            st.markdown(f"**Entrega:** {row['Fecha de entrega'].date() if pd.notnull(row['Fecha de entrega']) else '—'}")
            st.markdown(f"**Publicacion:** {row['Fecha de publicacion'].date() if pd.notnull(row['Fecha de publicacion']) else '—'}")
            cumplido = st.checkbox("✅ Marcar como cumplido", key=f"chk_{i}", value=(row['Estado'] == 'Hecho'))
            df.at[i, 'Estado'] = 'Hecho' if cumplido else 'Pendiente'
    except KeyError as e:
        st.warning(f"⚠️ Faltan columnas necesarias: {e}")

# Botón para guardar cambios
if st.button("💾 Guardar cambios"):
    df.to_excel(archivo_excel, index=False)
    st.success("Cambios guardados en el archivo.")