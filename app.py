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
from datetime import date, datetime

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

tabs = st.tabs(["Conversión", "Potencia", "Cupla", "Bobinado", "Ohm", "Ventas", "REP"])

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
            st.latex(r"T = F \cdot R")
            st.latex(r"P = \frac{T \cdot RPM}{716.2}")

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

# -------- TAB 7 (REP) --------
with tabs[6]:
    st.subheader("REPARACIONES")

    # ===== CONFIG =====
    moneda_rep = st.selectbox("Moneda", ["Pesos ($)", "Dólares (u$s)"], key="rep_moneda")
    simbolo = "$" if "Pesos" in moneda_rep else "u$s"

    # ===== USUARIO =====
    st.subheader("Datos del usuario")
    nombre_usuario_rep = st.text_input("Nombre y Apellido", key="rep_nombre")
    telefono_usuario_rep = st.text_input("Teléfono", key="rep_tel")
    email_usuario_rep = st.text_input("Email", key="rep_email")

    # ===== CLIENTE =====
    st.subheader("Datos del cliente")
    cliente_rep = st.text_input("Cliente", key="rep_cliente")
    contacto_rep = st.text_input("CONTACTO", key="rep_contacto")
    telefono_cliente_rep = st.text_input("Teléfono cliente", key="rep_tel_cliente")
    email_cliente_rep = st.text_input("Email cliente", key="rep_email_cliente")

    # ===== PRESUPUESTO =====
    st.subheader("Datos del presupuesto")
    numero_presupuesto = st.text_input("Presupuesto N°", "0001", key="rep_pres")
    referencia_rep = st.text_input("Referencia", key="rep_ref")

    # ===== DATOS TECNICOS =====
    st.subheader("Datos del equipo")
    modelo = st.text_input("Modelo", key="rep_modelo")
    potencia = st.number_input("Potencia", min_value=0.0, key="rep_pot")
    unidad_potencia = st.selectbox("Unidad de potencia", ["kW", "HP"], key="rep_unidad")
    velocidad = st.number_input("Velocidad (RPM)", min_value=0.0, key="rep_rpm")
    t_inducido = st.number_input("T. Inducido (V)", min_value=0.0, key="rep_ti")
    t_alimentacion = st.number_input("T. Alimentación (V)", min_value=0.0, key="rep_ta")
    forma = st.text_input("Forma Constructiva", key="rep_forma")
    proteccion = st.text_input("Protección Mecánica", key="rep_prot")
    aislacion = st.text_input("Aislación", key="rep_aisl")
    accesorios = st.text_input("Accesorios", key="rep_acc")
    numero = st.text_input("Número", key="rep_num")
    cantidad = st.number_input("Cantidad", min_value=1, value=1, key="rep_cant")
    faltantes = st.text_input("Faltantes", key="rep_falt")

    # ===== TEXTO AUTOMATICO =====
    partes = [f"{int(cantidad)} Motor"]
    if modelo: partes.append(modelo)
    if potencia: partes.append(f"{potencia} {unidad_potencia}")
    if velocidad: partes.append(f"{velocidad} RPM")
    if t_inducido: partes.append(f"{t_inducido} V")
    if t_alimentacion: partes.append(f"{t_alimentacion} V")
    if forma: partes.append(forma)
    if proteccion: partes.append(proteccion)
    if numero: partes.append(f"N° {numero}")

    texto_equipo = "Reparación " + ", ".join(partes)

    # ===== TAREAS =====
    st.subheader("TAREAS A REALIZAR")
    tareas = st.multiselect("Seleccionar tareas", [
        "Mantenimiento","Bobinado Rotor","Bobinado Estator","Bobinado Completo",
        "Mantenimiento Ventilación","Mantenimiento DT","Escobillas","Portaescobillas",
        "Colector","Conos de Mica","Cambio de eje"
    ], key="rep_tareas")

    precios_tareas = {}
    total_tareas = 0

    for t in tareas:
        precio = st.number_input(f"Precio - {t}", min_value=0.0, key=f"rep_t_{t}")
        precios_tareas[t] = precio
        total_tareas += precio

    # ===== TAREAS MANUALES =====
    st.markdown("### Tareas manuales")
    if "tareas_manuales_rep" not in st.session_state:
        st.session_state.tareas_manuales_rep = []

    if st.button("➕ Agregar tarea manual", key="rep_add"):
        st.session_state.tareas_manuales_rep.append("")

    for i in range(len(st.session_state.tareas_manuales_rep)):
        texto = st.text_input(f"Tarea manual {i+1}", key=f"rep_tm_{i}")
        precio = st.number_input(f"Precio tarea manual {i+1}", min_value=0.0, key=f"rep_tm_p_{i}")
        if texto:
            precios_tareas[texto] = precio
            total_tareas += precio

    # ===== REPUESTOS =====
    st.subheader("ELEMENTOS A REEMPLAZAR")
    repuestos = st.multiselect("Seleccionar elementos", [
        "Rodamientos","Escobillas","Portaescobillas","Resortes Escobillas",
        "Colector","Bornera","Ventilador","Terminales","Ferreteria","Varios"
    ], key="rep_repuestos")

    total_repuestos = 0
    for r in repuestos:
        precio = st.number_input(f"Precio - {r}", min_value=0.0, key=f"rep_r_{r}")
        total_repuestos += precio

    total_final = total_tareas + total_repuestos

    st.subheader("TOTAL")
    st.success(f"Total presupuesto: {simbolo} {total_final:,.2f}")

    # ===== PDF =====
    if st.button("📄 Generar PDF", key="rep_pdf"):

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        estilo_derecha = ParagraphStyle(name="derecha", parent=styles["Normal"], alignment=TA_RIGHT)

        contenido = []

        if os.path.exists("logohead.png"):
            contenido.append(Image("logohead.png", width=450, height=120))
            contenido.append(Spacer(1, 10))

        fecha = datetime.now()
        meses = ["enero","febrero","marzo","abril","mayo","junio",
                 "julio","agosto","septiembre","octubre","noviembre","diciembre"]

        fecha_texto = f"Buenos Aires, {fecha.day} de {meses[fecha.month-1]} de {fecha.year}"
        contenido.append(Paragraph(fecha_texto, estilo_derecha))

        contenido.append(Paragraph(f"Cliente: {cliente_rep}", styles["Normal"]))
        contenido.append(Paragraph(texto_equipo, styles["Normal"]))

        contenido.append(Paragraph(f"TOTAL: {simbolo} {total_final:,.2f}", styles["Heading2"]))

        doc.build(contenido)

        st.download_button("⬇ Descargar PDF", buffer.getvalue(), "reparacion.pdf", key="rep_dl")

st.caption("Desarrollado por SED con soporte IA")




