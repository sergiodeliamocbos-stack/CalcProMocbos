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

input {
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

    hp = st.number_input("HP", value=0.0)
    if st.button("Calcular kW"):
        st.success(f"{hp*0.746:.3f} kW")

    kw = st.number_input("kW", value=0.0)
    if st.button("Calcular HP"):
        st.success(f"{kw/0.746:.3f} HP")

# -------- TAB 2 --------
with tabs[1]:
    st.subheader("Potencia")

    if st.checkbox("Ver fórmula", key="chk_pot"):
        st.latex("HP = \\frac{T \\cdot RPM}{716.2}")

    t = st.number_input("Cupla (kgm)", value=0.0)
    rpm = st.number_input("RPM", value=0.0)

    if st.button("Calcular Potencia"):
        if rpm != 0:
            st.success(f"{(t*rpm)/716.2:.3f} HP")

# -------- TAB 3 --------
with tabs[2]:
    st.subheader("Cupla")

    if st.checkbox("Ver fórmula", key="chk_cupla"):
        st.latex("T = \\frac{HP \\cdot 716.2}{RPM}")

    hp2 = st.number_input("HP", value=0.0)
    rpm2 = st.number_input("RPM", value=0.0)

    if st.button("Calcular Cupla"):
        if rpm2 != 0:
            st.success(f"{(hp2*716.2)/rpm2:.3f} kgm")

    st.markdown("---")

    kgm = st.number_input("kgm")
    if st.button("kgm → Nm"):
        st.success(f"{kgm*9.81:.2f} Nm")

    nm = st.number_input("Nm")
    if st.button("Nm → kgm"):
        st.success(f"{nm/9.81:.2f} kgm")

# -------- TAB 4 --------
with tabs[3]:
    st.subheader("Bobinado")

    if st.checkbox("Ver fórmula", key="chk_bob"):
        st.latex("I = \\frac{P \\cdot 1000}{\\sqrt{3} \\cdot V \\cdot fp \\cdot η}")

    P = st.number_input("Potencia (kW)", value=0.0)
    V = st.number_input("Voltaje (V)", value=0.0)
    eta = st.number_input("Rendimiento", value=0.9)
    fp = st.number_input("Factor de potencia", value=0.85)
    f = st.number_input("Frecuencia (Hz)", value=50.0)

    st.markdown("### 🔧 Datos opcionales reales")
    S_real = st.number_input("Sección real del alambre (mm²)", value=0.0)
    N_real = st.number_input("Espiras reales", value=0)

    if st.button("Calcular Bobinado"):
        if V != 0:
            I = (P*1000)/(math.sqrt(3)*V*fp*eta)
            S = I / 4
            N = (V / f) * 2

            st.success(
                f"Corriente: {I:.2f} A\n"
                f"Sección calculada: {S:.2f} mm²\n"
                f"Espiras estimadas: {N:.0f}"
            )

            # -------- SEMAFOROS --------

            # FP
            if fp < 0.75:
                st.error("🔴 FP bajo")
            elif fp < 0.85:
                st.warning("🟡 FP medio")
            else:
                st.success("🟢 FP bueno")

            # Rendimiento
            if eta < 0.80:
                st.error("🔴 Bajo rendimiento")
            elif eta < 0.88:
                st.warning("🟡 Rendimiento medio")
            else:
                st.success("🟢 Buen rendimiento")

            # Sección (inteligente)
            if S_real > 0:
                if S_real < S:
                    st.error("🔴 Cable chico (riesgo)")
                elif S_real < S*1.2:
                    st.warning("🟡 Cable justo")
                else:
                    st.success("🟢 Cable correcto")
            else:
                st.info("ℹ️ Ingresar sección real para diagnóstico")

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    if st.checkbox("Ver fórmula", key="chk_ohm"):
        st.latex("V = I \\cdot R")

    V = st.number_input("Voltaje", value=0.0)
    I = st.number_input("Intensidad", value=0.0)
    R = st.number_input("Resistencia", value=0.0)

    if st.button("Calcular"):
        if V == 0:
            st.success(f"{I*R:.2f} V")
        elif I == 0:
            st.success(f"{V/R:.2f} A")
        elif R == 0:
            st.success(f"{V/I:.2f} Ω")

st.caption("Desarrollado por SED con soporte IA")
