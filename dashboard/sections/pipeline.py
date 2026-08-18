# dashboard/sections/pipeline.py

import streamlit as st
import plotly.express as px
import pandas as pd

def render(pipeline):

    def filtrar_rango_fechas(
        df,
        inicio,
        fin,
        fecha_col="process_date"
    ):
        if fecha_col not in df.columns:
            return df

        if inicio is None or fin is None:
            return df

        inicio = pd.Timestamp(inicio)
        fin = pd.Timestamp(fin)

        return df[
            (df[fecha_col] >= inicio)
            & (df[fecha_col] <= fin)
        ]

    extract_df = (
        pipeline
        .status_extract_distribution()
        .to_pandas()
    )

    fig = px.bar(
        extract_df,
        x="status_extract",
        y="total",
        color="status_extract",
        title="Estado de extracción",
        color_discrete_map={
            "SUCCESS": "#539a6c",
            "FAILED": "#b54747",
            "PENDING": "#d98c2b"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Estado Solar")

    solar_df = (
        pipeline
        .status_solar_distribution()
        .to_pandas()
    )

    fig = px.bar(
        solar_df,
        x="status_solar",
        y="total",
        color="status_solar",
        title="Estado Solar",
        color_discrete_sequence=[
            "#539a6c",
            "#b54747",
            "#d98c2b"
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Distribución de vectores")

    vector_df = (
        pipeline
        .vector_distribution()
        .to_pandas()
    )

    vector_df["label"] = (
        vector_df["has_vector"]
        .map(
            {
                True: "Con vector",
                False: "Sin vector"
            }
        )
    )

    fig = px.bar(
        vector_df,
        x="label",
        y="total",
        color="label",
        title="Distribución de vectores",
        color_discrete_map={
            "Con vector": "#5b4bb7",
            "Sin vector": "#9b8cf0"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Filtro temporal")

    trend_df = (
        pipeline
        .processing_trend()
        .to_pandas()
    )

    fecha_min = trend_df["process_date"].min()
    fecha_max = trend_df["process_date"].max()

    rango_fechas = st.date_input(
        "Seleccione rango de fechas",
        value=(fecha_min, fecha_max)
    )

    if (
        rango_fechas is None
        or len(rango_fechas) != 2
    ):
        st.warning(
            "Seleccione una fecha inicial y una fecha final."
        )
        st.stop()

    inicio, fin = rango_fechas

    trend_df = filtrar_rango_fechas(
            trend_df,
            inicio,
            fin
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
        "Procesamiento por worker"
    )

    worker_df = (
        pipeline
        .processing_trend_by_worker()
        .to_pandas()
    )

    worker_df = filtrar_rango_fechas(
        worker_df,
        inicio,
        fin
    )

    fig = px.line(
        worker_df,
        x="process_date",
        y="rolling_7d",
        color="worker_host",
        markers=True,
        title="Procesamiento por worker (media móvil 7 días)"
    )

    fig.update_traces(
        line=dict(width=3)
    )

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

    extract_worker_df = (
        pipeline
        .extract_status_by_worker()
        .to_pandas()
    )

    fig = px.bar(
        extract_worker_df,
        y="worker_host",
        x="total",
        color="status_extract",
        orientation="h",
        barmode="stack",
        title="Extracciones por worker",
        color_discrete_map={
            "SUCCESS": "#539a6c",
            "FAILED": "#b54747",
            "PENDING": "#d98c2b"
        }
    )

    fig.update_layout(
        yaxis_title="Worker",
        xaxis_title="Documentos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Estado Solar por worker"
    )

    solar_worker_df = (
        pipeline
        .solar_status_by_worker()
        .to_pandas()
    )

    fig = px.bar(
        solar_worker_df,
        y="worker_host",
        x="total",
        color="status_solar",
        orientation="h",
        barmode="stack",
        title="Estado Solar por worker",
        color_discrete_map={
            "SUCCESS": "#539a6c",
            "FAILED": "#b54747",
            "PENDING": "#d98c2b"
        }
    )

    fig.update_layout(
        yaxis_title="Worker",
        xaxis_title="Documentos"
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

    success_df = filtrar_rango_fechas(
        success_df,
        inicio,
        fin
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

    failed_df = filtrar_rango_fechas(
        failed_df,
        inicio,
        fin
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

    vectorized_df = filtrar_rango_fechas(
        vectorized_df,
        inicio,
        fin
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

    st.subheader(
    "Extracciones exitosas por worker"
    )

    success_worker_df = (
        pipeline
        .success_trend_by_worker()
        .to_pandas()
    )

    success_worker_df = filtrar_rango_fechas(
        success_worker_df,
        inicio,
        fin
    )

    fig = px.line(
        success_worker_df,
        x="process_date",
        y="rolling_7d",
        color="worker_host",
        markers=True,
        title="Promedio móvil (7 días) de extracciones exitosas"
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Extracciones fallidas por worker"
    )

    failed_worker_df = (
        pipeline
        .failed_trend_by_worker()
        .to_pandas()
    )

    failed_worker_df = filtrar_rango_fechas(
        failed_worker_df,
        inicio,
        fin
    )

    fig = px.line(
        failed_worker_df,
        x="process_date",
        y="rolling_7d",
        color="worker_host",
        markers=True,
        title="Promedio móvil (7 días) de extracciones fallidas"
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )