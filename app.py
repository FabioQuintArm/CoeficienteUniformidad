st.markdown("Introduce los caudales recogidos (en ml) por cada gotero. Se analizarán 20 goteros.")

caudales = []

with st.form("form_caudales"):
    cols = st.columns(4)  # 4 columnas en pantalla
    for i in range(20):
        col = cols[i % 4]
        with col:
            val = st.number_input(f"Gotero {i+1}", min_value=0.0, step=0.1, key=f"g{i+1}")
            caudales.append(val)
    submitted = st.form_submit_button("Calcular CU")

if submitted:
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
