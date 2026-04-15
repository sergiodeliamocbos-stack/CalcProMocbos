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

    if st.button("Ver curva Potencia vs RPM"):
        if t != 0:
            rpm_vals = list(range(100, 3001, 100))
            hp_vals = [(t*r)/716.2 for r in rpm_vals]
            data = pd.DataFrame({"RPM": rpm_vals, "HP": hp_vals})
            st.line_chart(data.set_index("RPM"))

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

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        kgm = st.number_input("kgm", value=0.0, key="kgm_conv")
        if st.button("kgm → Nm"):
            st.success(f"{kgm * 9.81:.2f} Nm")

    with col2:
        nm = st.number_input("Nm", value=0.0, key="nm_conv")
        if st.button("Nm → kgm"):
            st.success(f"{nm / 9.81:.2f} kgm")

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

                # -------- SEMAFOROS --------
                if I > 20:
                    st.error(f"🔴 Corriente ALTA")
                elif I > 15:
                    st.warning(f"🟡 Corriente MEDIA")
                else:
                    st.success(f"🟢 Corriente NORMAL")

                if fp < 0.75:
                    st.error("🔴 FP bajo")
                elif fp < 0.85:
                    st.warning("🟡 FP medio")
                else:
                    st.success("🟢 FP bueno")

                if eta < 0.80:
                    st.error("🔴 Bajo rendimiento")
                elif eta < 0.88:
                    st.warning("🟡 Rendimiento medio")
                else:
                    st.success("🟢 Buen rendimiento")

    with col2:
        st.markdown("### 📌 Referencias")

        st.markdown("""
**Factor de Potencia (FP)**
- 0.9  → Excelente  
- 0.85 → Bueno  
- 0.8  → Normal  
- 0.7  → Bajo  

**Rendimiento (η)**
- 0.90 → Excelente  
- 0.85 → Bueno  
- 0.80 → Normal  
- 0.75 → Bajo  

**Densidad de corriente**
- 3 – 5 A/mm²  

**Frecuencia**
- 50 Hz → Argentina  
- 60 Hz → Industrial  
""")

# -------- TAB 5 --------
with tabs[4]:
    st.subheader("Ley de Ohm")

    if st.checkbox("Ver fórmula", key="chk_ohm"):
        st.latex("V = I \\cdot R")

    V = st.number_input("Voltaje", value=0.0, key="v_ohm")
    I = st.number_input("Intensidad", value=0.0, key="i_ohm")
    R = st.number_input("Resistencia", value=0.0, key="r_ohm")

    ohm_res = st.empty()
    st.markdown("Resultado:")
    ohm_res.markdown("<div class='result-box'>---</div>", unsafe_allow_html=True)

    if st.button("Calcular"):
        if V == 0:
            ohm_res.markdown(f"<div class='result-box'>{I*R:.2f} V</div>", unsafe_allow_html=True)
        elif I == 0:
            ohm_res.markdown(f"<div class='result-box'>{V/R:.2f} A</div>", unsafe_allow_html=True)
        elif R == 0:
            ohm_res.markdown(f"<div class='result-box'>{V/I:.2f} Ω</div>", unsafe_allow_html=True)

st.caption("Desarrollado por SED")
