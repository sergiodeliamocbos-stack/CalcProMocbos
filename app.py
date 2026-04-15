import streamlit as st
import math
import pandas as pd

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

input[type="number"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

.result-box {
    background-color: #000000;
    color: #00ffcc;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-size: 18px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# -------- LOGO --------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("mocbos-alta2.jpg", width=180)

st.markdown("<h2 style='text-align:center;'>CalcPro Mocbos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Planta Mocbos</p>", unsafe_allow_html=True)

tabs = st.tabs(["Conversión", "Potencia", "Cupla", "Bobinado", "Ohm"])

# -------- TAB 1 --------
with tabs[0]:
    st.subheader("Conversión HP / kW")

    if st.checkbox("Ver fórmula", key="chk_conv"):
        st.latex("kW = HP \\times 0.746")
        st.latex("HP = \\frac{kW}{0.746}")

    hp = st.number_input("HP", value=0.0, key="hp_conv")

    kw_res = st.empty()
    st.markdown("kW:")
    kw_res.markdown("<div class='result-box'>0.000</div>", unsafe_allow_html=True)

    if st.button("Calcular kW"):
        kw = hp * 0.746
        kw_res.markdown(f"<div class='result-box'>{kw:.3f}</div>", unsafe_allow_html=True)

    kw = st.number_input("kW", value=0.0, key="kw_conv")

    hp_res = st.empty()
    st.markdown("HP:")
    hp_res.markdown("<div class='result-box'>0.000</div>", unsafe_allow_html=True)

    if st.button("Calcular HP"):
        hp_val = kw / 0.746
        hp_res.markdown(f"<div class='result-box'>{hp_val:.3f}</div>", unsafe_allow_html=True)

# -------- TAB 2 --------
with tabs[1]:
    st.subheader("Potencia")

    if st.checkbox("Ver fórmula", key="chk_pot"):
        st.latex("HP = \\frac{T \\cdot RPM}{716.2}")

    t = st.number_input("Cupla (kgm)", value=0.0, key="t_pot")
    rpm = st.number_input("RPM", value=0.0, key="rpm_pot")

    pot_res = st.empty()
    st.markdown("Potencia (HP):")
    pot_res.markdown("<div class='result-box'>0.000</div>", unsafe_allow_html=True)

    if st.button("Calcular Potencia"):
        if rpm != 0:
            hp_calc = (t*rpm)/716.2
            pot_res.markdown(f"<div class='result-box'>{hp_calc:.3f}</div>", unsafe_allow_html=True)

# -------- TAB 3 --------
with tabs[2]:
    st.subheader("Cupla")

    if st.checkbox("Ver fórmula", key="chk_cupla"):
        st.latex("T = \\frac{HP \\cdot 716.2}{RPM}")

    hp2 = st.number_input("HP", value=0.0, key="hp_cupla")
    rpm2 = st.number_input("RPM", value=0.0, key="rpm_cupla")

    cupla_res = st.empty()
    st.markdown("Cupla (kgm):")
    cupla_res.markdown("<div class='result-box'>0.000</div>", unsafe_allow_html=True)

    if st.button("Calcular Cupla"):
        if rpm2 != 0:
            t_calc = (hp2*716.2)/rpm2
            cupla_res.markdown(f"<div class='result-box'>{t_calc:.3f}</div>", unsafe_allow_html=True)

# -------- TAB 4 --------
with tabs[3]:
    st.subheader("Bobinado")

    P = st.number_input("Potencia (kW)", value=0.0)
    V = st.number_input("Voltaje (V)", value=0.0)
    eta = st.number_input("Rendimiento", value=0.9)
    fp = st.number_input("Factor de potencia", value=0.85)

    if st.button("Calcular Bobinado"):
        if V != 0:
            I = (P*1000)/(math.sqrt(3)*V*fp*eta)

            st.success(f"Corriente: {I:.2f} A")

            I_nominal = (P*1000)/(math.sqrt(3)*V*0.85*0.9)

            if I > I_nominal * 1.2:
                st.error("🔴 Corriente ALTA")
            elif I > I_nominal * 1.05:
                st.warning("🟡 Corriente MEDIA")
            else:
                st.success("🟢 Corriente NORMAL")

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    V = st.number_input("Voltaje", value=0.0, key="v_ohm")
    I = st.number_input("Intensidad", value=0.0, key="i_ohm")
    R = st.number_input("Resistencia", value=0.0, key="r_ohm")

    if st.button("Calcular"):
        if V == 0:
            st.success(f"{I*R:.2f} V")
        elif I == 0:
            st.success(f"{V/R:.2f} A")
        elif R == 0:
            st.success(f"{V/I:.2f} Ω")

st.caption("Desarrollado por SED")
