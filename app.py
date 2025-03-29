import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="Crédito Express", layout="wide")

from PIL import Image

# Mostrar logo
logo = Image.open("logo.png")
st.image(logo, width=150)


# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("prestamos_data").sheet1

# Función para cargar datos
@st.cache_data
def cargar_datos():
    return pd.DataFrame(sheet.get_all_records())

def guardar_datos(row):
    sheet.append_row(row)

# Navegación
menu = st.sidebar.radio("Menú Principal", ["📋 Registro de Clientes", "💰 Registro de Pagos", "🔍 Consulta", "📊 Reportes"])

# Registro de Cliente
if menu == "📋 Registro de Clientes":
    st.header("📝 Registro de nuevo cliente")

    with st.form("form_cliente"):
        nombre = st.text_input("Nombre del cliente")
        cedula = st.text_input("Cédula")
        celular = st.text_input("Celular")
        correo = st.text_input("Correo (opcional)")
        fecha = st.date_input("Fecha del préstamo", value=datetime.today())
        cuotas = st.selectbox("Número de cuotas", [1, 2, 3, 4])
        monto = st.number_input("Monto del préstamo", min_value=100000, step=50000)
        observaciones = st.text_area("Observaciones")
        enviar = st.form_submit_button("Registrar cliente")

        if enviar:
            if not (nombre and cedula and celular and monto):
                st.warning("⚠️ Por favor completa todos los campos obligatorios.")
            else:
                interes = 0.15
                total = monto * (1 + interes)
                comision = monto * 0.02
                datos = [nombre, cedula, celular, correo, fecha.strftime("%Y-%m-%d"), cuotas, monto, comision, total, observaciones, 0]
                guardar_datos(datos)
                st.success("✅ Cliente registrado con éxito.")

# Registro de Pagos
elif menu == "💰 Registro de Pagos":
    st.header("💵 Registrar pago de cuotas")

    cedula = st.text_input("Buscar cliente por cédula")
    df = cargar_datos()
    cliente = df[df["Cédula"] == cedula]

    if not cliente.empty:
        cliente = cliente.iloc[0]
        st.table(pd.DataFrame([{
            "Cliente": cliente["Nombre"],
            "Cuotas": cliente["Cuotas"],
            "Cuotas pagadas": cliente["Pagadas"],
            "Cuota mensual": round(cliente["Total a pagar"] / cliente["Cuotas"], 2),
            "Saldo restante": round(cliente["Total a pagar"] - (cliente["Pagadas"] * (cliente["Total a pagar"] / cliente["Cuotas"])), 2)
        }]))

        forma = st.radio("¿Cómo desea registrar el pago?", ["Por número de cuotas", "Por monto exacto"])
        if forma == "Por número de cuotas":
            n_cuotas = st.number_input("¿Cuántas cuotas está pagando?", min_value=1, max_value=int(cliente["Cuotas"] - cliente["Pagadas"]))
            if st.button("Registrar pago por cuotas"):
                nueva_pagadas = int(cliente["Pagadas"]) + int(n_cuotas)
                df.loc[df["Cédula"] == cedula, "Pagadas"] = nueva_pagadas
                sheet.clear()
                sheet.append_row(df.columns.tolist())
                for i in df.values.tolist():
                    sheet.append_row(i)
                st.success("✅ Pago registrado correctamente.")
    elif cedula:
        st.info("No se encontró ningún cliente con esa cédula.")

# Consulta
elif menu == "🔍 Consulta":
    st.header("🔍 Buscar cliente por nombre o cédula")
    query = st.text_input("Escriba nombre o cédula")

    if query:
        df = cargar_datos()
        resultados = df[df["Nombre"].str.contains(query, case=False) | df["Cédula"].astype(str).str.contains(query)]
        if not resultados.empty:
            st.dataframe(resultados)
        else:
            st.warning("No se encontraron coincidencias.")

# Reportes
elif menu == "📊 Reportes":
    st.header("📊 Reporte General")
    df = cargar_datos()

    if not df.empty:
        total_clientes = df.shape[0]
        total_ganancia = df["Total a pagar"].sum() - df["Monto"].sum()
        total_comision = df["Comisión"].sum()
        total_recaudo = df["Total a pagar"].sum()

        st.markdown(f"- 👥 **Total clientes registrados:** {total_clientes}")
        st.markdown(f"- 💰 **Ganancia neta total:** ${total_ganancia:,.0f}")
        st.markdown(f"- 🤝 **Comisión total pagada:** ${total_comision:,.0f}")
        st.markdown(f"- 🪙 **Total a recaudar:** ${total_recaudo:,.0f}")

        st.divider()
        st.subheader("📄 Tabla de Créditos")
        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Reporte')
        data_excel = output.getvalue()

        st.download_button(
            label="📥 Descargar Excel",
            data=data_excel,
            file_name="reporte_creditos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No hay datos para mostrar.")