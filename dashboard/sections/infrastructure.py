import streamlit as st


def render(infra):

    st.subheader(
        "Volumen por worker"
    )

    st.bar_chart(
        infra
        .worker_volume()
        .to_pandas()
        .set_index("worker_host")
    )

    st.subheader(
        "CPU promedio"
    )

    st.bar_chart(
        infra
        .worker_cpu()
        .to_pandas()
        .set_index("worker_host")
    )

    st.subheader(
        "Memoria promedio"
    )

    st.bar_chart(
        infra
        .worker_memory()
        .to_pandas()
        .set_index("worker_host")
    )

    st.subheader(
        "Duración promedio"
    )

    st.bar_chart(
        infra
        .worker_duration()
        .to_pandas()
        .set_index("worker_host")
    )