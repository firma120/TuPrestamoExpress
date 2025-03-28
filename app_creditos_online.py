
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Tu Préstamo Express", layout="centered")
st.markdown("<h1 style='text-align: center;'>💸 Tu Préstamo Express</h1>", unsafe_allow_html=True)

excel_file = "historial_creditos_online.xlsx"
capital = 500000
interes = 0.15
total_pagar = capital * (1 + interes)
comision_socio = capital * 0.02
ganancia_neta = total_pagar - capital - comision_socio

if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=["Cliente", "Cédula", "Celular", "Correo", "Fecha", "Cuotas", "Cuota mensual", "Comisión socio", "Ganancia neta", "Total a pagar"])

st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Registrar Cliente", "Ver Créditos"])

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
        df.to_excel(excel_file, index=False)
        st.success("✅ Cliente registrado con éxito.")

elif menu == "Ver Créditos":
    st.subheader("📊 Créditos Registrados")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No hay créditos registrados aún.")
