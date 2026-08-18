import streamlit as st
import plotly.express as px


def render(infra):

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Volumen por worker"
        )

        volume_df = (
            infra
            .worker_volume()
            .to_pandas()
        )

        fig = px.bar(
            volume_df,
            x="worker_host",
            y="total",
            color="worker_host",
            title="Volumen por worker"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Memoria promedio"
        )

        memory_df = (
            infra
            .worker_memory()
            .to_pandas()
        )

        fig = px.bar(
            memory_df,
            x="worker_host",
            y="avg_mem_mb",
            color="worker_host",
            title="Memoria promedio"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "CPU promedio"
        )

        cpu_df = (
            infra
            .worker_cpu()
            .to_pandas()
        )

        fig = px.bar(
            cpu_df,
            x="worker_host",
            y="avg_cpu_percent",
            color="worker_host",
            title="CPU promedio"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Duración promedio"
        )

        duration_df = (
            infra
            .worker_duration()
            .to_pandas()
        )

        fig = px.bar(
            duration_df,
            x="worker_host",
            y="avg_duration_seconds",
            color="worker_host",
            title="Duración promedio"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )