# CALCPRO MOCBOS - VERSION FINAL PRO COMPLETA

import streamlit as st
import math
import numpy as np
import pandas as pd
import os
from datetime import date, datetime
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.units import cm

st.set_page_config(page_title="CalcPro Mocbos", layout="wide")

# ===== ESTILO =====
st.markdown("""
<style>
.stApp { background-color: #1e1e1e; color: white; }
input { background-color: white !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ CalcPro Mocbos PRO")

# ===== TABS =====
tabs = st.tabs(["Conversión","Potencia","Cupla","Bobinado","Ohm","Ventas","REP"])

# =====================
# CONVERSION
# =====================
with tabs[0]:
    st.subheader("HP ↔ kW")

    if st.checkbox("Ver fórmula", key="c1"):
        st.latex("kW = HP \\cdot 0.746")
        st.latex("HP = \\frac{kW}{0.746}")

    hp = st.number_input("HP", key="hp1")
    if st.button("→ kW"):
        st.success(f"{hp*0.746:.3f} kW")

    kw = st.number_input("kW", key="kw1")
    if st.button("→ HP"):
        st.success(f"{kw/0.746:.3f} HP")

# =====================
# POTENCIA
# =====================
with tabs[1]:
    st.subheader("Potencia")

    if st.checkbox("Ver fórmula", key="p1"):
        st.latex("HP = \\frac{T \\cdot RPM}{716.2}")

    t = st.number_input("Cupla (kgm)", key="t1")
    rpm = st.number_input("RPM", key="rpm1")

    if st.button("Calcular Potencia"):
        if rpm != 0:
            hp_calc = (t*rpm)/716.2
            st.success(f"{hp_calc:.2f} HP")

            x = np.linspace(0, rpm*1.5 if rpm>0 else 1000, 50)
            y = (t*x)/716.2
            df = pd.DataFrame({"RPM":x, "HP":y}).set_index("RPM")
            st.line_chart(df)

# =====================
# CUPLA
# =====================
with tabs[2]:
    st.subheader("Cupla")

    if st.checkbox("Ver fórmula", key="c2"):
        st.latex("T = \\frac{HP \\cdot 716.2}{RPM}")

    hp2 = st.number_input("HP", key="hp2")
    rpm2 = st.number_input("RPM", key="rpm2")

    if st.button("Calcular Cupla"):
        if rpm2 != 0:
            st.success(f"{(hp2*716.2)/rpm2:.2f} kgm")

    st.markdown("---")

    kgm = st.number_input("kgm", key="kgm")
    if st.button("kgm → Nm"):
        st.success(f"{kgm*9.81:.2f} Nm")

    nm = st.number_input("Nm", key="nm")
    if st.button("Nm → kgm"):
        st.success(f"{nm/9.81:.2f} kgm")

# =====================
# BOBINADO
# =====================
with tabs[3]:
    st.subheader("Bobinado")

    col1, col2 = st.columns([2,1])

    with col1:
        if st.checkbox("Ver fórmula", key="b1"):
            st.latex("I = \\frac{P \\cdot 1000}{\\sqrt{3} \\cdot V \\cdot fp \\cdot η}")

        P = st.number_input("Potencia (kW)", key="p")
        V = st.number_input("Voltaje (V)", key="v")
        eta = st.number_input("Rendimiento", value=0.9, key="eta")
        fp = st.number_input("Factor de potencia", value=0.85, key="fp")
        f = st.number_input("Frecuencia", value=50.0, key="f")

        if st.button("Calcular Bobinado"):
            if V != 0:
                I = (P*1000)/(math.sqrt(3)*V*fp*eta)
                S = I/4
                N = (V/f)*2

                st.success(f"Corriente: {I:.2f} A")
                st.info(f"Sección: {S:.2f} mm²")
                st.info(f"Espiras: {N:.0f}")

    with col2:
        st.markdown("""
### 📊 Referencias

FP:
- 0.9 Excelente
- 0.85 Bueno
- 0.8 Normal

Rendimiento:
- 0.90 Excelente
- 0.85 Bueno
- 0.80 Normal
""")

# =====================
# OHM
# =====================
with tabs[4]:
    st.subheader("Ley de Ohm")

    if st.checkbox("Ver fórmula", key="o1"):
        st.latex("V = I \\cdot R")

    V2 = st.number_input("Voltaje", key="v2")
    I2 = st.number_input("Corriente", key="i2")
    R2 = st.number_input("Resistencia", key="r2")

    if st.button("Calcular Ohm"):
        if V2 == 0:
            st.success(f"{I2*R2:.2f} V")
        elif I2 == 0:
            st.success(f"{V2/R2:.2f} A")
        elif R2 == 0:
            st.success(f"{V2/I2:.2f} Ω")

# =====================
# VENTAS PRO
# =====================
with tabs[5]:
    st.subheader("VENTAS PRO")

    cliente = st.text_input("Cliente", key="v_cliente")
    presupuesto = st.text_input("Presupuesto N°", key="v_pres")
    importe = st.number_input("Importe", key="v_imp")

    if st.button("Generar PDF Ventas"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        contenido = []

        if os.path.exists("logohead.png"):
            contenido.append(Image("logohead.png", width=400, height=100))

        contenido.append(Paragraph(f"Cliente: {cliente}", styles["Normal"]))
        contenido.append(Paragraph(f"Presupuesto: {presupuesto}", styles["Normal"]))
        contenido.append(Paragraph(f"Importe: {importe}", styles["Normal"]))

        doc.build(contenido)

        st.download_button("Descargar PDF", buffer.getvalue(), "ventas.pdf")

# =====================
# REP PRO
# =====================
with tabs[6]:
    st.subheader("REPARACIONES PRO")

    cliente_r = st.text_input("Cliente", key="r_cliente")
    tarea = st.text_input("Tarea", key="r_tarea")
    costo = st.number_input("Costo", key="r_costo")

    if st.button("Generar PDF REP"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        contenido = []

        if os.path.exists("logohead.png"):
            contenido.append(Image("logohead.png", width=400, height=100))

        contenido.append(Paragraph(f"Cliente: {cliente_r}", styles["Normal"]))
        contenido.append(Paragraph(f"Trabajo: {tarea}", styles["Normal"]))
        contenido.append(Paragraph(f"Costo: {costo}", styles["Normal"]))

        doc.build(contenido)

        st.download_button("Descargar PDF", buffer.getvalue(), "rep.pdf")

st.caption("Desarrollado por SED con soporte IA")




