
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Tu Préstamo Express", layout="centered")
st.markdown("<h1 style='text-align: center;'>💸 Tu Préstamo Express</h1>", unsafe_allow_html=True)

archivo = "historial_creditos_online.xlsx"
capital = 500000
interes = 0.15
total_pagar = capital * (1 + interes)
comision_socio = capital * 0.02
ganancia_neta = total_pagar - capital - comision_socio

if os.path.exists(archivo):
    df = pd.read_excel(archivo)
else:
    df = pd.DataFrame(columns=["Cliente", "Cédula", "Celular", "Correo", "Fecha", "Cuotas", "Cuota mensual", "Comisión socio", "Ganancia neta", "Total a pagar"])

st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Registrar Cliente", "Ver Créditos", "Consulta de Clientes", "Reportes"])

if menu == "Registrar Cliente":
    st.subheader("📝 Registro de nuevo cliente")
    nombre = st.text_input("Nombre del cliente")
    cedula = st.text_input("Cédula")
    celular = st.text_input("Celular")
    correo = st.text_input("Correo")
    fecha = st.date_input("Fecha del préstamo", value=datetime.today())
    cuotas = st.selectbox("Número de cuotas", [1, 2, 3, 4])
    if st.button("Registrar"):
        cuota_mensual = total_pagar / cuotas
        nuevo = {
            "Cliente": nombre,
            "Cédula": cedula,
            "Celular": celular,
            "Correo": correo,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Cuotas": cuotas,
            "Cuota mensual": cuota_mensual,
            "Comisión socio": comision_socio,
            "Ganancia neta": ganancia_neta,
            "Total a pagar": total_pagar
        }
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_excel(archivo, index=False)
        st.success("✅ Cliente registrado con éxito.")

elif menu == "Ver Créditos":
    st.subheader("📊 Créditos Registrados")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No hay créditos registrados aún.")

elif menu == "Consulta de Clientes":
    st.subheader("🔍 Buscar cliente")
    if not df.empty:
        filtro = st.text_input("Buscar por nombre o cédula")
        if filtro:
            resultado = df[df["Cliente"].str.lower().str.contains(filtro.lower()) | df["Cédula"].astype(str).str.contains(filtro)]
            if not resultado.empty:
                st.dataframe(resultado)
            else:
                st.warning("No se encontró ningún cliente.")
        else:
            st.info("Escribe algo para buscar.")
    else:
        st.info("No hay datos registrados.")

elif menu == "Reportes":
    st.subheader("📈 Reporte General")
    if not df.empty:
        st.write(f"👥 Total clientes registrados: {len(df)}")
        st.write(f"💸 Ganancia neta total: ${df['Ganancia neta'].sum():,.0f}")
        st.write(f"🤝 Comisión total pagada: ${df['Comisión socio'].sum():,.0f}")
        st.write(f"💰 Total a recaudar: ${df['Total a pagar'].sum():,.0f}")
    else:
        st.info("No hay datos para generar reportes.")
