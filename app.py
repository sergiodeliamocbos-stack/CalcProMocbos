# CALCPRO MOCBOS - VERSION FINAL COMPLETA FUNCIONAL

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

st.title("⚡ CalcPro Mocbos PRO")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Conversión","Potencia","Cupla","Bobinado","Ohm","Ventas","REP"
])

# ================= CONVERSION =================
with tab1:
    st.subheader("Conversión HP / kW")

    if st.checkbox("Ver fórmula", key="f_conv"):
        st.latex("kW = HP \\cdot 0.746")
        st.latex("HP = \\frac{kW}{0.746}")

    hp = st.number_input("HP", value=0.0, key="hp_conv")
    st.success(f"kW: {hp*0.746:.3f}")

    kw = st.number_input("kW", value=0.0, key="kw_conv")
    st.success(f"HP: {kw/0.746:.3f}")

# ================= POTENCIA =================
with tab2:
    st.subheader("Cálculo de Potencia")

    if st.checkbox("Ver fórmula", key="f_pot"):
        st.latex("HP = \\frac{T \\cdot RPM}{716.2}")

    torque = st.number_input("Cupla (kgm)", value=0.0, key="torque_pot")
    rpm = st.number_input("RPM", value=0.0, key="rpm_pot")

    if rpm > 0:
        hp_calc = (torque * rpm) / 716.2
        st.success(f"Potencia: {hp_calc:.2f} HP")

        x = np.linspace(0, rpm*1.5, 50)
        y = (torque * x) / 716.2
        df = pd.DataFrame({"RPM": x, "HP": y}).set_index("RPM")
        st.line_chart(df)

# ================= CUPLA =================
with tab3:
    st.subheader("Cálculo de Cupla")

    if st.checkbox("Ver fórmula", key="f_cupla"):
        st.latex("T = \\frac{HP \\cdot 716.2}{RPM}")

    hp2 = st.number_input("HP", value=0.0, key="hp_cupla")
    rpm2 = st.number_input("RPM", value=0.0, key="rpm_cupla")

    if rpm2 > 0:
        st.success(f"Cupla: {(hp2*716.2)/rpm2:.2f} kgm")

    st.markdown("---")

    kgm = st.number_input("kgm", value=0.0, key="kgm")
    st.info(f"Nm: {kgm*9.81:.2f}")

    nm = st.number_input("Nm", value=0.0, key="nm")
    st.info(f"kgm: {nm/9.81:.2f}")

# ================= BOBINADO =================
with tab4:
    st.subheader("Cálculo de Bobinado")

    col1, col2 = st.columns([2,1])

    with col1:
        if st.checkbox("Ver fórmula", key="f_bob"):
            st.latex("I = \\frac{P \\cdot 1000}{\\sqrt{3} \\cdot V \\cdot fp \\cdot η}")

        P = st.number_input("Potencia (kW)", value=0.0, key="bob_p")
        V = st.number_input("Voltaje (V)", value=0.0, key="bob_v")
        eta = st.number_input("Rendimiento", value=0.9, key="bob_eta")
        fp = st.number_input("Factor de potencia", value=0.85, key="bob_fp")
        f = st.number_input("Frecuencia", value=50.0, key="bob_freq")

        if V > 0:
            I = (P*1000)/(math.sqrt(3)*V*fp*eta)
            S = I/4
            N = (V/f)*2

            st.success(f"Corriente: {I:.2f} A")
            st.info(f"Sección: {S:.2f} mm²")
            st.info(f"Espiras: {N:.0f}")

    with col2:
        st.markdown("""
### REFERENCIAS

FP:
0.9 Excelente
0.85 Bueno
0.8 Normal
0.7 Bajo

Rendimiento:
0.90 Excelente
0.85 Bueno
0.80 Normal
0.75 Bajo
""")

# ================= OHM =================
with tab5:
    st.subheader("Ley de Ohm")

    if st.checkbox("Ver fórmula", key="f_ohm"):
        st.latex("V = I \\cdot R")

    V2 = st.number_input("Voltaje", value=0.0, key="ohm_v")
    I2 = st.number_input("Corriente", value=0.0, key="ohm_i")
    R2 = st.number_input("Resistencia", value=0.0, key="ohm_r")

    if V2 == 0:
        st.success(f"Voltaje: {I2*R2:.2f} V")
    elif I2 == 0:
        st.success(f"Corriente: {V2/R2:.2f} A")
    elif R2 == 0:
        st.success(f"Resistencia: {V2/I2:.2f} Ω")

# ================= VENTAS =================
with tab6:
    st.subheader("VENTAS")

    # USUARIO
    st.markdown("### Datos usuario")
    nombre_usuario = st.text_input("Nombre", key="ven_user")
    email_usuario = st.text_input("Email", key="ven_mail")
    telefono_usuario = st.text_input("Teléfono", key="ven_tel")

    # CLIENTE
    st.markdown("### Datos cliente")
    fecha = st.date_input("Fecha", value=date.today(), key="ven_fecha")
    cliente = st.text_input("Cliente", key="ven_cliente")
    contacto = st.text_input("Contacto", key="ven_contacto")
    tel_cliente = st.text_input("Teléfono", key="ven_tel_cli")
    email_cliente = st.text_input("Email", key="ven_email_cli")
    presupuesto = st.text_input("Presupuesto N°", key="ven_pres")
    referencia = st.text_input("Referencia", key="ven_ref")

    col1, col2 = st.columns(2)
    with col1:
        moneda = st.selectbox("Moneda", ["$","U$S"], key="ven_moneda")
    with col2:
        importe = st.number_input("Importe", key="ven_importe")

    st.markdown("---")

    # CALCULO MOTOR
    st.subheader("Cálculo motor sugerido")

    peso = st.number_input("Peso (kg)", key="ven_peso")
    diametro = st.number_input("Diámetro (m)", key="ven_diam")

    modo = st.radio("Modo velocidad", ["RPM","Tiempo"], key="ven_modo")

    if modo == "RPM":
        rpm_salida = st.number_input("RPM carga", key="ven_rpm")
    else:
        distancia = st.number_input("Distancia (m)", key="ven_dist")
        tiempo = st.number_input("Tiempo (s)", value=1.0, key="ven_time")
        rpm_salida = (distancia/tiempo)/(math.pi*diametro)*60 if diametro>0 else 0

    reductor = st.checkbox("Tiene reductor", key="ven_red")

    if reductor:
        relacion = st.number_input("Relación", value=10.0, key="ven_rel")
    else:
        relacion = None

    if st.button("Calcular motor"):
        if peso>0 and diametro>0 and rpm_salida>0:
            radio = diametro/2
            fuerza = peso*9.81
            torque = fuerza*radio

            if reductor:
                rpm_motor = rpm_salida*relacion
            else:
                rpm_motor = 1500
                relacion = rpm_motor/rpm_salida

            hp = (torque*rpm_motor)/716.2

            st.success(f"Motor sugerido: {round(hp)} HP")
            st.info(f"RPM motor: {rpm_motor:.0f}")
            st.info(f"Relación: {relacion:.2f}")
            st.info(f"Torque: {torque:.2f} Nm")

# ================= REP =================
with tab7:
    st.subheader("REPARACIONES")

    cliente = st.text_input("Cliente", key="rep_cliente")
    contacto = st.text_input("Contacto", key="rep_contacto")

    tareas = st.multiselect("Tareas", [
        "Mantenimiento","Bobinado Rotor","Bobinado Estator","Bobinado Completo",
        "Ventilación","Escobillas","Rodamientos"
    ], key="rep_tareas")

    total = 0
    for t in tareas:
        precio = st.number_input(f"Precio {t}", key=f"rep_{t}")
        total += precio

    st.success(f"TOTAL: {total}")

st.caption("Desarrollado por SED")





