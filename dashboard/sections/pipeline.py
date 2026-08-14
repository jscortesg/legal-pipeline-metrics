# dashboard/sections/pipeline.py

import streamlit as st
import plotly.express as px

def render(pipeline):

    st.subheader("Estado de extracción")

    st.bar_chart(
        pipeline
        .status_extract_distribution()
        .to_pandas()
        .set_index("status_extract")
    )

    st.subheader("Estado Solar")

    st.bar_chart(
        pipeline
        .status_solar_distribution()
        .to_pandas()
        .set_index("status_solar")
    )

    st.subheader("Distribución de vectores")

    st.bar_chart(
        pipeline
        .vector_distribution()
        .to_pandas()
        .set_index("has_vector")
    )

    st.subheader("Tendencia de procesamiento")

    trend_df = (
        pipeline
        .processing_trend()
        .to_pandas()
    )

    fig = px.line(
        trend_df,
        x="process_date",
        y=["total", "rolling_7d"],
        markers=True,
        title="Procesamiento diario"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    fig.data[0].line.color = "#147582"
    fig.data[1].line.color = "#539a6c"

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Extracción por worker"
    )

    worker_df = (
        pipeline
        .extract_status_by_worker()
        .to_pandas()
    )

    fig = px.bar(
        worker_df,
        x="worker_host",
        y="total",
        color="status_extract",
        barmode="stack",
        title="Extracciones por worker"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Estado Solar por worker"
    )

    solar_df = (
        pipeline
        .solar_status_by_worker()
        .to_pandas()
    )

    fig = px.bar(
        solar_df,
        x="worker_host",
        y="total",
        color="status_solar",
        barmode="stack",
        title="Estado Solar por worker"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Extracciones exitosas"
    )

    success_df = (
        pipeline
        .extract_success_trend()
        .to_pandas()
    )

    fig = px.line(
        success_df,
        x="process_date",
        y=["total", "rolling_7d"],
        markers=True,
        title="Extracciones exitosas"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    fig.data[0].line.color = "#147582"
    fig.data[1].line.color = "#539a6c"

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Tendencia de fallos"
    )

    failed_df = (
        pipeline
        .extract_failed_trend()
        .to_pandas()
    )

    fig = px.line(
        failed_df,
        x="process_date",
        y=["total", "rolling_7d"],
        markers=True,
        title="Extracciones fallidas"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    fig.data[0].line.color = "#b54747"
    fig.data[1].line.color = "#d98c2b"

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Tendencia de vectorización"
    )

    vectorized_df = (
        pipeline
        .vectorized_trend()
        .to_pandas()
    )

    fig = px.line(
        vectorized_df,
        x="process_date",
        y=["total", "rolling_7d"],
        markers=True,
        title="Documentos vectorizados"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    fig.data[0].line.color = "#5b4bb7"
    fig.data[1].line.color = "#8d7df0"

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )