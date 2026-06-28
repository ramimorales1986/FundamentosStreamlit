import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

st.set_page_config(
    page_title="Análisis de Riesgo Crediticio",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Dashboard de Riesgo Crediticio")
st.markdown("### Maestría en Tecnologías de Información - Big Data & Analytics")

# ==========================
# CARGA DEL DATASET
# ==========================

@st.cache_data
def cargar_datos():
    df = pd.read_csv("Creditos_Ecuador_60000_Registros.csv")
    return df

df = cargar_datos()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Filtros")

ciudad = st.sidebar.multiselect(
    "Ciudad",
    options=sorted(df["Ciudad"].unique()),
    default=sorted(df["Ciudad"].unique())
)

estado = st.sidebar.multiselect(
    "Estado del Crédito",
    options=df["Estado_Credito"].unique(),
    default=df["Estado_Credito"].unique()
)

vivienda = st.sidebar.multiselect(
    "Tipo de Vivienda",
    options=df["Tipo_Vivienda"].unique(),
    default=df["Tipo_Vivienda"].unique()
)

df = df[
    (df["Ciudad"].isin(ciudad)) &
    (df["Estado_Credito"].isin(estado)) &
    (df["Tipo_Vivienda"].isin(vivienda))
]

# ==========================
# KPIs
# ==========================

total = len(df)
aprobados = len(df[df["Estado_Credito"] == "Aprobado"])
rechazados = len(df[df["Estado_Credito"] == "Rechazado"])

ingreso = df["Ingreso_Anual"].mean()
score = df["Score_Crediticio"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Clientes", f"{total:,}")
c2.metric("Aprobados", f"{aprobados:,}")
c3.metric("Rechazados", f"{rechazados:,}")
c4.metric("Ingreso Promedio", f"${ingreso:,.0f}")
c5.metric("Score Promedio", f"{score:.0f}")

st.divider()

# ==========================
# HISTOGRAMA
# ==========================

fig = px.histogram(
    df,
    x="Ingreso_Anual",
    nbins=40,
    title="Distribución del Ingreso Anual"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# BARRAS POR CIUDAD
# ==========================

ciudades = (
    df["Ciudad"]
    .value_counts()
    .reset_index()
)

ciudades.columns = ["Ciudad", "Clientes"]

fig = px.bar(
    ciudades,
    x="Ciudad",
    y="Clientes",
    title="Clientes por Ciudad"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# PIE CHART
# ==========================

fig = px.pie(
    df,
    names="Estado_Credito",
    title="Estado del Crédito"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
