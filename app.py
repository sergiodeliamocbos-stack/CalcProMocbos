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
button[data-baseweb="tab"] { background-color: #2b2b2b !important; color: white !important; }
button[data-baseweb="tab"][aria-selected="true"] { background-color: #444 !important; color: #00ffcc !important; }
.stButton>button { background-color: #00a86b; color: white; border-radius: 6px; height: 45px; width: 100%; font-weight: bold; }
input { background-color: #ffffff !important; color: #000000 !important; }
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
            rpm_range = np.linspace(0, rpm*1.5 if rpm > 0 else 1000, 50)
            potencia_curve = (t * rpm_range) / 716.2
            df = pd.DataFrame({"RPM": rpm_range, "Potencia (HP)": potencia_curve}).set_index("RPM")
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

# -------- TAB 6 (VENTAS ORIGINAL INTEGRADA) --------
with tabs[5]:
    st.subheader("VENTAS")

    # ===== ESTADOS =====
    if "resultado_v" not in st.session_state:
        st.session_state.resultado_v = None
    if "pdf_v" not in st.session_state:
        st.session_state.pdf_v = None

    # ===== DATOS USUARIO =====
    st.subheader("Datos del usuario")
    nombre_usuario = st.text_input("Nombre y Apellido", key="v_nombre")
    email_usuario = st.text_input("Email", key="v_email")
    telefono_usuario = st.text_input("Teléfono", key="v_tel")

    # ===== DATOS CLIENTE =====
    st.subheader("Datos del cliente / presupuesto")

    fecha = st.date_input("FECHA", value=date.today(), key="v_fecha")
    cliente = st.text_input("CLIENTE (Nombre o Razón Social)", key="v_cliente")
    email_cliente = st.text_input("EMAIL", key="v_email_cliente")
    telefono = st.text_input("TELÉFONO", key="v_tel_cliente")
    presupuesto = st.text_input("Presupuesto N°", key="v_presupuesto")
    referencia = st.text_input("Referencia (N° reparación)", key="v_ref")
    contacto = st.text_input("CONTACTO (Nombre y Apellido)", key="v_contacto")

    col1, col2 = st.columns(2)
    with col1:
        moneda = st.selectbox("Moneda", ["$", "U$S"], key="v_moneda")
    with col2:
        importe = st.text_input("IMPORTE", key="v_importe")

    nombre_archivo = st.text_input("Nombre del archivo PDF", "reporte_motor", key="v_nombre_archivo")

    # ===== DATOS TECNICOS =====
    st.subheader("Datos de entrada")

    peso = st.number_input("Peso (kg)", min_value=0.0, key="v_peso")
    diametro = st.number_input("Diámetro (m)", min_value=0.0, key="v_diam")

    tipo = st.selectbox("Tipo de aplicación", ["Elevación", "Cinta", "Ventilador"], key="v_tipo")

    modo_velocidad = st.radio("¿Cómo definir velocidad?", ["RPM", "Tiempo"], key="v_modo")

    if modo_velocidad == "RPM":
        rpm_salida = st.number_input("RPM en la carga", min_value=0.0, key="v_rpm")
    else:
        distancia = st.number_input("Distancia (m)", min_value=0.0, key="v_dist")
        tiempo = st.number_input("Tiempo (s)", min_value=0.1, key="v_tiempo")

        if diametro > 0:
            circ = 3.1416 * diametro
            vel = distancia / tiempo
            rpm_salida = (vel / circ) * 60
        else:
            rpm_salida = 0

    # ===== REDUCTOR =====
    tiene_reductor = st.checkbox("Tengo reductor", key="v_reductor")

    if tiene_reductor:
        relacion_usuario = st.number_input("Relación de reductor", min_value=1.0, value=10.0, key="v_rel")
    else:
        relacion_usuario = None

    mostrar_formula = st.checkbox("Mostrar fórmula utilizada", key="v_formula")

    # ===== FUNCION FECHA =====
    def fecha_texto(f):
        meses = ["enero","febrero","marzo","abril","mayo","junio",
                 "julio","agosto","septiembre","octubre","noviembre","diciembre"]
        return f"Buenos Aires, {f.day} de {meses[f.month-1]}, de {f.year}"

    # ===== CALCULO =====
    if st.button("Calcular", key="v_calc"):

        if peso > 0 and diametro > 0 and rpm_salida > 0:

            radio = diametro / 2
            fuerza = peso * 9.81
            torque = fuerza * radio

            if tiene_reductor:
                rpm_motor = rpm_salida * relacion_usuario
                relacion = relacion_usuario
            else:
                rpm_motor = 1500
                relacion = rpm_motor / rpm_salida

            hp = (torque * rpm_motor) / 716.2

            st.session_state.resultado_v = {
                "hp": round(hp),
                "rpm": rpm_motor,
                "relacion": relacion,
                "torque": torque
            }

    # ===== RESULTADOS =====
    if st.session_state.resultado_v:

        r = st.session_state.resultado_v

        st.success(f"Motor sugerido: {r['hp']} HP")
        st.info(f"RPM motor: {r['rpm']:.0f}")
        st.info(f"Relación reductor: {r['relacion']:.2f}")
        st.info(f"Torque: {r['torque']:.2f} Nm")

        if mostrar_formula:
            st.markdown("### Fórmulas utilizadas")
            st.latex(r"T = F \\cdot R")
            st.latex(r"P = \\frac{T \\cdot RPM}{716.2}")

        # ===== PDF =====
        if st.button("📄 Generar informe PDF", key="v_pdf"):

            buffer = BytesIO()

            doc = SimpleDocTemplate(buffer, leftMargin=1.5*cm, rightMargin=2*cm)

            styles = getSampleStyleSheet()
            style_right = ParagraphStyle(name="Right", parent=styles["Normal"], alignment=TA_RIGHT)

            contenido = []

            # LOGO CORREGIDO
            if os.path.exists("logohead.png"):
                img = Image("logohead.png", width=14*cm)
                img.hAlign = "CENTER"
                contenido.append(img)
                contenido.append(Spacer(1, 10))

            izquierda = f"""
<b>Cliente:</b> {cliente}<br/>
Email: {email_cliente}<br/>
Tel: {telefono}
"""

            derecha = f"""
{fecha_texto(fecha)}<br/>
Presupuesto N°: {presupuesto}<br/>
Referencia: {referencia}<br/>
Contacto: {contacto}
"""

            contenido.append(Table(
                [[Paragraph(izquierda, styles["Normal"]),
                  Paragraph(derecha, style_right)]],
                colWidths=[10*cm, 6*cm]
            ))

            contenido.append(Spacer(1, 15))

            contenido.append(Paragraph("De nuestra mayor consideración:", styles["Normal"]))
            contenido.append(Spacer(1, 10))

            contenido.append(Paragraph(
                "Según los datos proporcionados y los cálculos realizados, se recomienda lo siguiente:",
                styles["Normal"]
            ))

            contenido.append(Spacer(1, 15))

            contenido.append(Paragraph(f"Motor: {r['hp']} HP", styles["Normal"]))

            contenido.append(Spacer(1, 20))

            if importe:
                contenido.append(Paragraph(
                    f"<b>Precio Unitario. .................................. {moneda} {importe}</b>",
                    style_right
                ))

            contenido.append(Spacer(1, 15))

            nota = """
NOTA 1: Los precios indicados no incluyen IVA y se entienden en nuestro depósito de Buenos Aires.<br/><br/>
DATOS BANCARIO:<br/>
Cta. Cte. en Pesos<br/>
Bco. Frances<br/>
N°: 010- 00-7478/9<br/>
MOTORTECH S.A.<br/>
CBU 01 700 107 20000000 747893<br/>
CUIT 30-70733456-4<br/><br/>
Plazo de entrega: A CONVENIR
"""
            contenido.append(Paragraph(nota, styles["Normal"]))

            contenido.append(Spacer(1, 20))

            if nombre_usuario:
                contenido.append(Paragraph(f"<b>{nombre_usuario}</b>", styles["Normal"]))
                contenido.append(Paragraph(email_usuario, styles["Normal"]))
                if telefono_usuario:
                    contenido.append(Paragraph(f"Tel.Cel: {telefono_usuario}", styles["Normal"]))

            contenido.append(Paragraph("<b>MOTORTECH S.A.</b>", styles["Normal"]))

            doc.build(contenido)

            st.session_state.pdf_v = buffer.getvalue()

    # ===== DESCARGA =====
    if st.session_state.pdf_v:
        st.download_button(
            "⬇ Descargar PDF",
            st.session_state.pdf_v,
            file_name=f"{nombre_archivo}.pdf",
            mime="application/pdf",
            key="v_download"
        )

st.caption("Desarrollado por SED con soporte IA")


