import streamlit as st
import plotly.express as px


def render(inventory):

    mag_df = (
    inventory
    .documentos_por_magistrado()
    .to_pandas()
    )

    magistrados = ["Todos"] + sorted(
        mag_df["magistrado_fiscal"].tolist()
    )

    magistrado = st.selectbox(
        "Filtrar por magistrado",
        magistrados
    )

    magistrado_filtro = (
        None
        if magistrado == "Todos"
        else magistrado
    )

    st.subheader(
        "Anexos por tipo de archivo"
    )

    tipo_df = (
        inventory
        .anexos_por_tipo_archivo(
            magistrado_filtro
        )
        .to_pandas()
    )

    fig = px.bar(
        tipo_df,
        x="tipo_archivo",
        y="total",
        color="tipo_archivo",
        title="Anexos por tipo de archivo"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Documentos por reparto"
    )

    reparto_df = (
        inventory
        .documentos_por_reparto(
            magistrado_filtro
        )
        .to_pandas()
    )

    fig = px.bar(
        reparto_df,
        x="reparto",
        y="total",
        color="reparto",
        title="Documentos por reparto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if magistrado_filtro is None:

        st.subheader(
                "Documentos por magistrado"
        )

        mag_df = (
            inventory
            .documentos_por_magistrado()
            .to_pandas()
        )

        fig = px.bar(
            mag_df,
            x="magistrado_fiscal",
            y="total",
            color="magistrado_fiscal",
            title="Documentos por magistrado"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )