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

# Asegurar que las fechas están en formato datetime
df['Recordatorio'] = pd.to_datetime(df['Recordatorio'], dayfirst=True, errors='coerce')
df['Fecha de entrega'] = pd.to_datetime(df['Fecha de entrega'], dayfirst=True, errors='coerce')
df['Fecha de publicación'] = pd.to_datetime(df['Fecha de publicación'], dayfirst=True, errors='coerce')

# Agregar columna "Estado" si no existe
if 'Estado' not in df.columns:
    df['Estado'] = 'Pendiente'

st.set_page_config(page_title="Gestión de Boletines", layout="wide")
st.title("🗞️ Panel de Gestión de Boletines")

hoy = pd.to_datetime(datetime.today().date())

# Alertas importantes
st.subheader("🔔 Alertas del día")

alertas = df[
    ((df['Recordatorio'] <= hoy) & (df['Estado'] == 'Pendiente')) |
    ((df['Fecha de entrega'] < hoy) & (df['Estado'] == 'Pendiente'))
]

if alertas.empty:
    st.success("No hay alertas por hoy. Todo en orden.")
else:
    st.warning("Tienes entregas con recordatorio o vencidas:")
    st.dataframe(alertas)

# Mostrar y editar cada trabajo
st.subheader("📋 Lista de trabajos")
for i, row in df.iterrows():
    with st.expander(f"📌 {row['Tema/Materia']} | {row['Tipo de Boletin']} | {row['Responsable']}"):
        st.markdown(f"**Instancia/Oficina:** {row['instancia/oficina']}")
        st.markdown(f"**Número de boletín:** {row['número boletín']}")
        st.markdown(f"**Recordatorio:** {row['Recordatorio'].date() if pd.notnull(row['Recordatorio']) else '—'}")
        st.markdown(f"**Entrega:** {row['Fecha de entrega'].date() if pd.notnull(row['Fecha de entrega']) else '—'}")
        st.markdown(f"**Publicación:** {row['Fecha de publicación'].date() if pd.notnull(row['Fecha de publicación']) else '—'}")
        cumplido = st.checkbox("✅ Marcar como cumplido", key=f"chk_{i}", value=(row['Estado'] == 'Hecho'))
        df.at[i, 'Estado'] = 'Hecho' if cumplido else 'Pendiente'

# Botón para guardar cambios
if st.button("💾 Guardar cambios"):
    df.to_excel(archivo_excel, index=False)
    st.success("Cambios guardados en el archivo.")