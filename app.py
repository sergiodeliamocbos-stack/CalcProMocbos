import streamlit as st
import math
import pandas as pd

st.set_page_config(
    page_title="CalcPro Mocbos",
    layout="centered",
    page_icon="⚡"
)

# -------- ESTILO INDUSTRIAL --------
st.markdown("""
    <style>

    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }

    button[data-baseweb="tab"] {
        background-color: #2b2b2b !important;
        color: white !important;
        border-radius: 5px 5px 0px 0px;
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

    input[type="number"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #999 !important;
        border-radius: 5px !important;
        padding: 5px !important;
    }

    label {
        color: #ffffff !important;
        font-weight: 500;
    }

    </style>
""", unsafe_allow_html=True)

# -------- LOGO --------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("mocbos-alta2.jpg", width=180)

st.markdown("<h2 style='text-align:center;'>CalcPro Mocbos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Planta Mocbos - Herramienta de cálculo eléctrico</p>", unsafe_allow_html=True)

tabs = st.tabs(["Conversión", "Potencia", "Cupla", "Bobinado", "Ohm"])

# -------- TAB 1 --------
with tabs[0]:
    st.subheader("Conversión HP / kW")

    hp = st.number_input("HP", value=0.0, step=1.0, key="hp_conv")
    if st.button("Calcular kW"):
        st.success(f"{hp * 0.746:.3f} kW")

    kw = st.number_input("kW", value=0.0, step=1.0, key="kw_conv")
    if st.button("Calcular HP"):
        st.success(f"{kw / 0.746:.3f} HP")

# -------- TAB 2 --------
with tabs[1]:
    st.subheader("Potencia")

    t = st.number_input("Cupla (kgm)", value=0.0, step=0.5, key="t_pot")
    rpm = st.number_input("RPM", value=0.0, step=100.0, key="rpm_pot")

    if st.button("Calcular Potencia"):
        if rpm != 0:
            hp = (t * rpm) / 716.2
            st.success(f"{hp:.3f} HP")

    st.markdown("---")

    if st.button("Ver curva Potencia vs RPM"):
        if t != 0:
            rpm_vals = list(range(100, 3001, 100))
            hp_vals = [(t * r) / 716.2 for r in rpm_vals]

            data = pd.DataFrame({
                "RPM": rpm_vals,
                "HP": hp_vals
            })

            st.line_chart(data.set_index("RPM"))
        else:
            st.warning("Ingresar cupla para generar curva")

# -------- TAB 3 --------
with tabs[2]:
    st.subheader("Cupla")

    hp2 = st.number_input("HP", value=0.0, step=1.0, key="hp_cupla")
    rpm2 = st.number_input("RPM", value=0.0, step=100.0, key="rpm_cupla")

    if st.button("Calcular Cupla"):
        if rpm2 != 0:
            st.success(f"{(hp2 * 716.2) / rpm2:.3f} kgm")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        kgm = st.number_input("kgm", value=0.0, step=0.5, key="kgm_conv")
        if st.button("Convertir a Nm"):
            st.success(f"{kgm * 9.81:.3f} Nm")

    with col2:
        nm = st.number_input("Nm", value=0.0, step=1.0, key="nm_conv")
        if st.button("Convertir a kgm"):
            st.success(f"{nm / 9.81:.3f} kgm")

# -------- TAB 4 --------
with tabs[3]:
    st.subheader("Bobinado")

    col1, col2 = st.columns([2,1])

    with col1:
        P = st.number_input("Potencia (kW)", value=0.0, step=1.0, key="p_bob")
        V = st.number_input("Voltaje (V)", value=0.0, step=10.0, key="v_bob")
        eta = st.number_input("Rendimiento (0-1)", value=0.9, step=0.01, key="eta_bob")
        fp = st.number_input("Factor de potencia (0-1)", value=0.85, step=0.01, key="fp_bob")
        f = st.number_input("Frecuencia (Hz)", value=50.0, step=1.0, key="f_bob")

        if st.button("Calcular Bobinado"):
            if V != 0:
                I = (P * 1000) / (math.sqrt(3) * V * fp * eta)
                S = I / 4
                N = (V / f) * 2

                st.success(f"{I:.2f} A | {S:.2f} mm² | {N:.0f} espiras")

    with col2:
        st.markdown("### 📌 Referencias")

        st.markdown("""
        **Factor de potencia (fp):**
        - 0.75 → motores chicos  
        - 0.80–0.85 → estándar  
        - 0.90 → alto rendimiento  

        **Rendimiento (η):**
        - 0.80 → bajo  
        - 0.85–0.90 → normal  
        - 0.92 → eficiente  

        **Densidad de corriente:**
        - 3–5 A/mm² → uso típico  

        **Frecuencia:**
        - 50 Hz → estándar AR  
        - 60 Hz → industrial  
        """)

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    V = st.number_input("Voltaje (V)", value=0.0, step=10.0, key="v_ohm")
    I = st.number_input("Intensidad (A)", value=0.0, step=0.5, key="i_ohm")
    R = st.number_input("Resistencia (Ohm)", value=0.0, step=1.0, key="r_ohm")

    if st.button("Calcular"):
        if V == 0 and I != 0 and R != 0:
            st.success(f"V = {I * R:.2f} Volts")
        elif I == 0 and V != 0 and R != 0:
            st.success(f"I = {V / R:.2f} Amper")
        elif R == 0 and V != 0 and I != 0:
            st.success(f"R = {V / I:.2f} Ohms")
        else:
            st.warning("Ingresar solo 2 valores")

st.markdown("---")
st.caption("Desarrollado por SED con soporte IA")
