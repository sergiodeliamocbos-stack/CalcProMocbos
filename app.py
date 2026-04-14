import streamlit as st
import math

st.set_page_config(page_title="CalcPro Mocbos", layout="centered")

# -------- LOGO CENTRADO --------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("mocbos-alta2.jpg", width=200)

st.title("⚡ CalcPro Mocbos - Planta Mocbos")

tabs = st.tabs(["Conversión", "Potencia", "Cupla", "Bobinado", "Ohm"])

# -------- TAB 1 --------
with tabs[0]:
    st.subheader("Conversión HP / kW")

    hp = st.number_input("HP", value=0.0, key="hp1")
    if st.button("Calcular kW"):
        st.success(f"{hp * 0.746:.3f} kW")

    kw = st.number_input("kW", value=0.0, key="kw1")
    if st.button("Calcular HP"):
        st.success(f"{kw / 0.746:.3f} HP")

# -------- TAB 2 --------
with tabs[1]:
    st.subheader("Potencia")

    t = st.number_input("Cupla (kgm)", value=0.0, key="t1")
    rpm = st.number_input("RPM", value=0.0, key="rpm1")

    if st.button("Calcular Potencia"):
        if rpm != 0:
            st.success(f"{(t*rpm)/716.2:.3f} HP")

# -------- TAB 3 --------
with tabs[2]:
    st.subheader("Cupla")

    hp2 = st.number_input("HP", value=0.0, key="hp2")
    rpm2 = st.number_input("RPM", value=0.0, key="rpm2")

    if st.button("Calcular Cupla"):
        if rpm2 != 0:
            st.success(f"{(hp2*716.2)/rpm2:.3f} kgm")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        kgm = st.number_input("kgm", value=0.0, key="kgm1")
        if st.button("→ Nm"):
            st.success(f"{kgm*9.81:.3f} Nm")

    with col2:
        nm = st.number_input("Nm", value=0.0, key="nm1")
        if st.button("→ kgm"):
            st.success(f"{nm/9.81:.3f} kgm")

# -------- TAB 4 --------
with tabs[3]:
    st.subheader("Bobinado")

    P = st.number_input("Potencia (kW)", value=0.0, key="p1")
    V = st.number_input("Voltaje (V)", value=0.0, key="v1")
    eta = st.number_input("Rendimiento (0-1)", value=0.9, key="eta1")
    fp = st.number_input("Factor de potencia (0-1)", value=0.85, key="fp1")
    f = st.number_input("Frecuencia (Hz)", value=50.0, key="f1")

    if st.button("Calcular Bobinado"):
        if V != 0:
            I = (P*1000)/(math.sqrt(3)*V*fp*eta)
            S = I/4
            N = (V/f)*2

            st.success(f"{I:.2f} A | {S:.2f} mm² | {N:.0f} espiras")

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    V = st.number_input("Voltaje (V)", value=0.0, key="v_ohm")
    I = st.number_input("Intensidad (A)", value=0.0, key="i_ohm")
    R = st.number_input("Resistencia (Ohm)", value=0.0, key="r_ohm")

    if st.button("Calcular Ohm"):
        if V == 0 and I != 0 and R != 0:
            st.success(f"V = {I*R:.2f} Volts")
        elif I == 0 and V != 0 and R != 0:
            st.success(f"I = {V/R:.2f} Amper")
        elif R == 0 and V != 0 and I != 0:
            st.success(f"R = {V/I:.2f} Ohms")
        else:
            st.warning("Ingresar solo 2 valores")

st.markdown("---")
st.caption("Desarrollado por SED con soporte IA")