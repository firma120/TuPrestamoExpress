
# 🦁 Crédito Express

**Crédito Express** es una aplicación web simple y elegante desarrollada con [Streamlit](https://streamlit.io), diseñada para gestionar microcréditos de forma rápida, segura y sin complicaciones.

---

## 🚀 Funcionalidades

✅ **Registro de Clientes**  
Formulario para registrar nuevos clientes con validación de campos (excepto correo).  
Incluye nombre, cédula, celular, fecha del préstamo, número de cuotas, monto y observaciones.

✅ **Registro de Pagos**  
Permite registrar pagos por número de cuotas y visualizar el historial del cliente: cuotas pagadas, saldo pendiente y valor por cuota.

✅ **Consulta de Clientes**  
Búsqueda en tiempo real por **nombre o cédula**.  
Muestra toda la información del cliente de forma clara y ordenada.

✅ **Reportes Generales**  
- Totales de clientes registrados, ganancias, comisiones y saldo por recaudar  
- Tabla general con todos los registros  
- Botón para **descargar reporte en Excel (.xlsx)**

---

## 📦 Cómo instalar y ejecutar

1. **Clona este repositorio:**

```bash
git clone https://github.com/tu_usuario/credito-express.git
cd credito-express
```

2. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

3. **Ejecuta la app:**

```bash
streamlit run app.py
```

---

## 🧠 Tecnología

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)
- [Pillow](https://python-pillow.org/) (para mostrar el logo)

---

## ✨ Vista previa

![Vista previa](logo.png)

---

## 🦁 Autor

**León Darío Orrego Espejo**  
Microemprendedor y desarrollador en formación.  
Medellín - Colombia 🇨🇴

---

## 💡 ¿Futuras mejoras?

- Conexión a Google Sheets
- Alertas por WhatsApp o email
- Control de pagos más detallado
- Exportación de reportes mensuales por cliente

---

📌 Este proyecto es ideal para microempresarios que quieren digitalizar su gestión sin complicarse.
