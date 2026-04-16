import streamlit as st
import math
import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.units import cm
from io import BytesIO
import os
from datetime import date

st.set_page_config(page_title="CalcPro Mocbos", layout="centered", page_icon="⚡")

# -------- ESTILO --------
st.markdown("""
<style>
.stApp { background-color: #1e1e1e; color: #ffffff; }

button[data-baseweb="tab"] {
    background-color: #2b2b2b !important;
    color: white !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #444 !important;
    color: #00ffcc !important;
}

.stButton>button {
    background-color: #00a86b;
    color: white;
    border-radius: 6px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

input {
    background-color: #ffffff !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# -------- LOGO --------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("mocbos-alta2.jpg", width=180)

st.markdown("<h2 style='text-align:center;'>CalcPro Mocbos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Planta Mocbos</p>", unsafe_allow_html=True)

tabs = st.tabs(["Conversión", "Potencia", "Cupla", "Bobinado", "Ohm", "Ventas"])

# -------- TAB 1 --------
with tabs[0]:
    st.subheader("Conversión HP / kW")

    if st.checkbox("Ver fórmula", key="chk_conv"):
        st.latex("kW = HP \\times 0.746")
        st.latex("HP = \\frac{kW}{0.746}")

    hp = st.number_input("HP", value=0.0, key="hp_conv")
    if st.button("Calcular kW", key="btn_kw"):
        st.success(f"{hp*0.746:.3f} kW")

    kw = st.number_input("kW", value=0.0, key="kw_conv")
    if st.button("Calcular HP", key="btn_hp"):
        st.success(f"{kw/0.746:.3f} HP")

# -------- TAB 2 --------
with tabs[1]:
    st.subheader("Potencia")

    if st.checkbox("Ver fórmula", key="chk_pot"):
        st.latex("HP = \\frac{T \\cdot RPM}{716.2}")

    t = st.number_input("Cupla (kgm)", value=0.0, key="t_pot")
    rpm = st.number_input("RPM", value=0.0, key="rpm_pot")

    if st.button("Calcular Potencia", key="btn_pot"):
        if rpm != 0:
            hp_calc = (t*rpm)/716.2
            st.success(f"{hp_calc:.3f} HP")

            st.markdown("### 📈 Curva Potencia vs RPM")
            rpm_range = np.linspace(0, rpm*1.5 if rpm > 0 else 1000, 50)
            potencia_curve = (t * rpm_range) / 716.2

            df = pd.DataFrame({
                "RPM": rpm_range,
                "Potencia (HP)": potencia_curve
            }).set_index("RPM")

            st.line_chart(df)

# -------- TAB 3 --------
with tabs[2]:
    st.subheader("Cupla")

    if st.checkbox("Ver fórmula", key="chk_cupla"):
        st.latex("T = \\frac{HP \\cdot 716.2}{RPM}")

    hp2 = st.number_input("HP", value=0.0, key="hp_cupla")
    rpm2 = st.number_input("RPM", value=0.0, key="rpm_cupla")

    if st.button("Calcular Cupla", key="btn_cupla"):
        if rpm2 != 0:
            st.success(f"{(hp2*716.2)/rpm2:.3f} kgm")

    st.markdown("---")

    kgm = st.number_input("kgm", key="kgm_conv")
    if st.button("kgm → Nm", key="btn_kgm_nm"):
        st.success(f"{kgm*9.81:.2f} Nm")

    nm = st.number_input("Nm", key="nm_conv")
    if st.button("Nm → kgm", key="btn_nm_kgm"):
        st.success(f"{nm/9.81:.2f} kgm")

# -------- TAB 4 --------
with tabs[3]:
    st.subheader("Bobinado")

    col1, col2 = st.columns([2,1])

    with col1:
        if st.checkbox("Ver fórmula", key="chk_bob"):
            st.latex("I = \\frac{P \\cdot 1000}{\\sqrt{3} \\cdot V \\cdot fp \\cdot η}")

        P = st.number_input("Potencia (kW)", value=0.0, key="p_bob")
        V = st.number_input("Voltaje (V)", value=0.0, key="v_bob")
        eta = st.number_input("Rendimiento", value=0.9, key="eta_bob")
        fp = st.number_input("Factor de potencia", value=0.85, key="fp_bob")
        f = st.number_input("Frecuencia (Hz)", value=50.0, key="f_bob")

        st.markdown("### 🔧 Datos opcionales reales")
        S_real = st.number_input("Sección real del alambre (mm²)", value=0.0, key="sreal_bob")
        N_real = st.number_input("Espiras reales", value=0, key="nreal_bob")

        if st.button("Calcular Bobinado", key="btn_bob"):
            if V != 0:
                I = (P*1000)/(math.sqrt(3)*V*fp*eta)
                S = I / 4
                N = (V / f) * 2

                st.success(f"Corriente: {I:.2f} A\nSección: {S:.2f} mm²\nEspiras: {N:.0f}")

    with col2:
        st.markdown("### 📌 Referencias")
        st.markdown("FP: 0.9 excelente / 0.85 bueno / 0.8 normal")

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    if st.checkbox("Ver fórmula", key="chk_ohm"):
        st.latex("V = I \\cdot R")

    V = st.number_input("Voltaje", value=0.0, key="v_ohm")
    I = st.number_input("Intensidad", value=0.0, key="i_ohm")
    R = st.number_input("Resistencia", value=0.0, key="r_ohm")

    if st.button("Calcular", key="btn_ohm"):
        if V == 0:
            st.success(f"{I*R:.2f} V")
        elif I == 0:
            st.success(f"{V/R:.2f} A")
        elif R == 0:
            st.success(f"{V/I:.2f} Ω")

# -------- TAB 6 --------
with tabs[5]:
    st.subheader("VENTAS")

    st.info("Herramienta de cálculo y generación de presupuesto")

    nombre_usuario = st.text_input("Nombre y Apellido", key="v_nombre")
    email_usuario = st.text_input("Email", key="v_email")
    telefono_usuario = st.text_input("Teléfono", key="v_tel")

    cliente = st.text_input("CLIENTE", key="v_cliente")
    presupuesto = st.text_input("Presupuesto N°", key="v_pres")

    moneda = st.selectbox("Moneda", ["$", "U$S"], key="v_moneda")
    importe = st.text_input("IMPORTE", key="v_importe")

    if st.button("Generar PDF", key="v_pdf"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        contenido = []

        # LOGO CORREGIDO
        if os.path.exists("logohead.png"):
            img = Image("logohead.png", width=14*cm)
            img.hAlign = "CENTER"
            contenido.append(img)
            contenido.append(Spacer(1, 10))

        contenido.append(Paragraph(f"Cliente: {cliente}", styles["Normal"]))
        contenido.append(Paragraph(f"Presupuesto: {presupuesto}", styles["Normal"]))
        contenido.append(Paragraph(f"Precio: {moneda} {importe}", styles["Normal"]))

        doc.build(contenido)
        st.download_button("Descargar PDF", buffer.getvalue(), "presupuesto.pdf")

st.caption("Desarrollado por SED")


