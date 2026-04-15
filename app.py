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
        f = st.number_input("Frecuencia (Hz)", value=50.0, key="freq_bob")

        if st.button("Calcular Bobinado"):
            if V != 0:
                I = (P*1000)/(math.sqrt(3)*V*fp*eta)
                S = I / 4
                N = (V / f) * 2

                st.success(
                    f"Corriente: {I:.2f} A\n"
                    f"Sección: {S:.2f} mm²\n"
                    f"Espiras: {N:.0f}"
                )

                # -------- SEMAFORO INTELIGENTE --------
                I_nominal = (P*1000)/(math.sqrt(3)*V*0.85*0.9)

                if I > I_nominal * 1.2:
                    st.error(f"🔴 Corriente ALTA (>{I_nominal*1.2:.1f} A)")
                elif I > I_nominal * 1.05:
                    st.warning(f"🟡 Corriente algo elevada")
                else:
                    st.success(f"🟢 Corriente NORMAL")

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

    with col2:
        st.markdown("### 📌 Referencias")
        st.markdown("""
FP: 0.9 excelente / 0.85 bueno / 0.8 normal  
η: 0.90 excelente / 0.85 bueno  
Densidad: 3–5 A/mm²  
Frecuencia: 50 Hz AR  
""")

st.caption("Desarrollado por SED con soporte IA")
