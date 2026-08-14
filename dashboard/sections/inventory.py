import streamlit as st


def render(inventory):

    st.subheader(
        "Anexos por tipo de archivo"
    )

    st.bar_chart(
        inventory
        .anexos_por_tipo_archivo()
        .to_pandas()
        .set_index("tipo_archivo")
    )

    st.subheader(
        "Documentos por reparto"
    )

    st.bar_chart(
        inventory
        .documentos_por_reparto()
        .to_pandas()
        .set_index("reparto")
    )

    st.subheader(
        "Documentos por magistrado"
    )

    st.bar_chart(
        inventory
        .documentos_por_magistrado()
        .to_pandas()
        .set_index("magistrado_fiscal")
    )