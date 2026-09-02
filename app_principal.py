import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent)) 

import streamlit as st
import pandas as pd

from src.componente_datos import cargar_y_validar_datos_agro
from src.componente_metrica import calcular_kpis_agro
from src.componente_prediccion import estimar_necesidad_riego

st.set_page_config(
    page_title="Agrotech smartFarm Sentinel",
    page_icon="🪴",
    layout="wide"
)

st.title("🪴 AgroTech SmartFarm sentinel")
st.subheader("Monitoreo IoT de humedad del Suelo y Predicción de Riego")
st.write(
    "Visualizza en tiempo real la humedad del suelo,la temperatura ambiente,"
    "Las parcelas críticas y la predicción de riego automático."
)

#Iniciamos el estado de la sesión para conservar los datos entre interacciones
if "datos_agro" not in st.session_state:
    st.session_state.datos_agro = pd.DataFrame()

st.sidebar.title("Menú")
st.sidebar.markdown("---")

archivo = st.sidebar.file_uploader(
    "📁 Selecciona un archivo CSV",
    type=["csv"]
)
st.sidebar.markdown("---")
st.sidebar.info(
        "Sube un archivo CSV para visualizar los datos de telemetría agrónoma."
    )

    #------------------------------------------------------------------------------------
    #Componente 1 :Ingesta y Validacion de datos
    #------------------------------------------------------------------------------------
if archivo:
            try:
                    st.session_state.datos_agro =cargar_y_validar_datos_agro(archivo)
                    st.sidebar.success("✅ Componente de Datos:ingesta y validación exitosas.")
            except Exception as e:
                    st.sidebar.error(f"❌ Fallo en la interfaz de datos :{e}")

df = st.session_state.datos_agro

#-------------------------------------------------------------
# Si hay datos disponible , se activan los componentes visuales
#-------------------------------------------------------
    
if not df.empty:
        st.markdown("---")

        st.markdown("###🔍 Filtro por Identificador de Parcela")

        parcelas_disponibles = ["Todas"] + sorted(df["id_parcela"].unique().tolist())
        parcela_seleccionada = st.selectbox("Selecciona una parcela", parcelas_disponibles)

        if parcela_seleccionada == "Todas":
         df_filtrado = df
        else:
         df_filtrado = df[df["id_parcela"] == parcela_seleccionada]

    # --------------------------------------------------------------------------
    # Componente 2: Métricas y KPIs
    # --------------------------------------------------------------------------
        st.markdown("### 📊 Panel Operativo")
        prom_humedad, max_temp, parcelas_criticas = calcular_kpis_agro(df_filtrado)
        col1, col2, col3 = st.columns(3)
        col1.metric("Humedad Promedio", f"{prom_humedad}%")
        col2.metric("Temp. Máxima", f"{max_temp} °C")
        col3.metric("Parcelas Críticas", f"{parcelas_criticas}")

    # --------------------------------------------------------------------------
    # Componente 3: Motor de Recomendación
    # --------------------------------------------------------------------------
        st.markdown("### 📊 Panel Operativo")
        prom_humedad, max_temp, parcelas_criticas = calcular_kpis_agro(df_filtrado)

        col1, col2, col3 = st.columns(3)
        col1.metric("Humedad Promedio", f"{prom_humedad}%")
        col2.metric("Temp. Máxima", f"{max_temp} °C")
        col3.metric("Parcelas Críticas", f"{parcelas_criticas}")

    # --------------------------------------------------------------------------
    # Componente 3: Motor de Recomendación
    # --------------------------------------------------------------------------
        st.markdown("### 💧 Motor de Recomendación de Riego")
        litros_necesarios = estimar_necesidad_riego(df_filtrado)

        if litros_necesarios > 0:
         st.warning(f"⚠️ **Alerta de Sequía**: Se requiere un riego estimado de **{litros_necesarios:.2f} Litros** de agua.")
        else:
          st.success("✅ **Estado Óptimo**: La humedad promedio es superior al 40%. No se requiere riego.")

    # --------------------------------------------------------------------------
    # Gráfico de Tendencia
    # --------------------------------------------------------------------------
        st.markdown("### 📈 Tendencia de Humedad en el Tiempo")
        st.line_chart(df_filtrado.set_index("timestamp")["humedad_suelo_pct"])

