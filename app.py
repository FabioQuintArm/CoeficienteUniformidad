import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Cálculo CU Riego por Goteo", layout="centered")

st.title("💧 Cálculo del Coeficiente de Uniformidad (CU)")
st.subheader("Sistema de riego por goteo")

st.markdown("Introduce los caudales recogidos (en ml) por cada gotero. Se analizarán 20 goteros.")

# Entrada organizada por filas (tabulador en orden)
caudales = []
contador = 0
for fila in range(5):  # 5 filas de 4 columnas
    cols = st.columns(4)
    for col in cols:
        with col:
            val = st.number_input(f"Gotero {contador + 1}", min_value=0.0, step=0.1, key=f"g{contador + 1}")
            caudales.append(val)
            contador += 1

# Botón para calcular CU
if st.button("Calcular CU"):
    caudales_ordenados = sorted(caudales)
    n = len(caudales_ordenados)
    media_total = np.mean(caudales_ordenados)
    n_cuartil = max(1, int(n * 0.25))
    media_cuartil_bajo = np.mean(caudales_ordenados[:n_cuartil])
    CU = 100 * (media_cuartil_bajo / media_total)

    # Interpretación
    if CU > 90:
        interpretacion = "Uniformidad excelente"
    elif CU > 85:
        interpretacion = "Uniformidad buena"
    elif CU > 80:
        interpretacion = "Uniformidad aceptable"
    elif CU > 75:
        interpretacion = "Uniformidad deficiente"
    else:
        interpretacion = "Uniformidad muy deficiente"

    # Guardar en session_state
    st.session_state.resultado = {
        "cu": CU,
        "media_total": media_total,
        "media_cuartil_bajo": media_cuartil_bajo,
        "interpretacion": interpretacion,
        "caudales": caudales
    }

# Mostrar resultados si existen
if "resultado" in st.session_state:
    r = st.session_state.resultado

    st.subheader("🔍 Resultado del cálculo")
    st.metric("Coeficiente de Uniformidad (CU)", f"{r['cu']:.2f} %")
    st.write(f"**Interpretación técnica:** {r['interpretacion']}")
    st.write(f"**Nº de goteros analizados:** {len(r['caudales'])}")
    st.write(f"**Media total:** {r['media_total']:.2f} ml")
    st.write(f"**Media del 25% más bajo:** {r['media_cuartil_bajo']:.2f} ml")

    def generar_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        textobject = c.beginText(50, 800)
        textobject.setFont("Helvetica", 12)

        textobject.textLine("Informe de Cálculo del Coeficiente de Uniformidad (CU)")
        textobject.textLine("")
        textobject.textLine(f"Número de goteros analizados: {len(r['caudales'])}")
        textobject.textLine(f"Media total: {r['media_total']:.2f} ml")
        textobject.textLine(f"Media del 25% más bajo: {r['media_cuartil_bajo']:.2f} ml")
        textobject.textLine(f"CU (Coeficiente de Uniformidad): {r['cu']:.2f} %")
        textobject.textLine(f"Interpretación: {r['interpretacion']}")
        textobject.textLine("")
        textobject.textLine("Caudales analizados (ml):")

        for i in range(0, len(r['caudales']), 5):
            bloque = ", ".join(f"{v:.1f}" for v in r['caudales'][i:i+5])
            textobject.textLine(bloque)

        c.drawText(textobject)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf = generar_pdf()
    st.download_button(
        label="📄 Descargar informe en PDF",
        data=pdf,
        file_name="informe_CU_riego_goteo.pdf",
        mime="application/pdf"
    )

    if st.checkbox("📊 Mostrar gráfico de caudales"):
        st.bar_chart(pd.Series(r['caudales'], name="Caudal (ml)"))

    if st.checkbox("📄 Mostrar tabla de datos"):
        df = pd.DataFrame(r['caudales'], columns=["Caudal (ml)"])
        st.dataframe(df)


