import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import polars as pl
import streamlit as st

from data_loader import load_metrics

from sections.pipeline import render as render_pipeline
from sections.inventory import render as render_inventory
from sections.infrastructure import render as render_infrastructure


st.set_page_config(
    page_title="Legal Pipeline Metrics",
    layout="wide"
)

st.title("Legal Pipeline Metrics")

metrics = load_metrics()

inventory = metrics["inventory"]
pipeline = metrics["pipeline"]
infrastructure = metrics["infrastructure"]


# =========================
# KPIs
# =========================

inventory_summary = inventory.summary()

documentos = inventory_summary["documentos"]

vector_df = pipeline.vector_distribution()

vectores = (
    vector_df
    .filter(pl.col("has_vector"))
    .get_column("total")
    .sum()
    if vector_df.height > 0
    else 0
)

workers = (
    infrastructure
    .worker_volume()
    .height
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Documentos",
        documentos
    )

with col2:
    st.metric(
        "Vectores",
        vectores
    )

with col3:
    st.metric(
        "Workers",
        workers
    )


# =========================
# TABS
# =========================

tab1, tab2, tab3 = st.tabs(
    [
        "Pipeline",
        "Inventario",
        "Infraestructura"
    ]
)

with tab1:
    render_pipeline(pipeline)

with tab2:
    render_inventory(inventory)

with tab3:
    render_infrastructure(infrastructure)