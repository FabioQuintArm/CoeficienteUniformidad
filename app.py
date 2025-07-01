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

caudales = []
cols = st.columns(4)
for i in range(20):
    col = cols[i % 4]
    with col:
        val = st.number_input(f"Gotero {i+1}", min_value=0.0, step=0.1, key=f"g{i+1}")
        caudales.append(val)

if st.button("Calcular CU"):
    caudales_ordenados = sorted(caudales)
    n = len(caudales_ordenados)
    media_total = np.mean(caudales_ordenados)
    n_cuartil = max(1, int(n * 0.25))
    media_cuartil_bajo = np.mean(caudales_ordenados[:n_cuartil])
    CU = 100 * (media_cuartil_bajo / media_total)

    st.subheader("🔍 Resultado del cálculo")
    st.metric("Coeficiente de Uniformidad (CU)", f"{CU:.2f} %")

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

    st.write(f"**Interpretación técnica:** {interpretacion}")
    st.write(f"**Nº de goteros analizados:** {n}")
    st.write(f"**Media total:** {media_total:.2f} ml")
    st.write(f"**Media del 25% más bajo:** {media_cuartil_bajo:.2f} ml")

    def generar_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        textobject = c.beginText(50, 800)
        textobject.setFont("Helvetica", 12)

        textobject.textLine("Informe de Cálculo del Coeficiente de Uniformidad (CU)")
        textobject.textLine("")
        textobject.textLine(f"Número de goteros analizados: {n}")
        textobject.textLine(f"Media total: {media_total:.2f} ml")
        textobject.textLine(f"Media del 25% más bajo: {media_cuartil_bajo:.2f} ml")
        textobject.textLine(f"CU (Coeficiente de Uniformidad): {CU:.2f} %")
        textobject.textLine(f"Interpretación: {interpretacion}")
        textobject.textLine("")
        textobject.textLine("Caudales analizados (ml):")

        for i in range(0, len(caudales), 5):
            bloque = ", ".join(f"{v:.1f}" for v in caudales[i:i+5])
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
        st.bar_chart(pd.Series(caudales, name="Caudal (ml)"))

    if st.checkbox("📄 Mostrar tabla de datos"):
        df = pd.DataFrame(caudales, columns=["Caudal (ml)"])
        st.dataframe(df)
