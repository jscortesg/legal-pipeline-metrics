# visualize/dashboard.py

from visualize.bar import BarPlot
from visualize.grouped_bar import GroupedBarPlot
from visualize.timeline import TimelineChart
from visualize.histogram import HistogramChart


class DashboardCharts:

    def __init__(
        self,
        inventory,
        pipeline,
        infrastructure
    ):

        self.inventory = inventory
        self.pipeline = pipeline
        self.infrastructure = infrastructure

        self.bar = BarPlot()
        self.grouped = GroupedBarPlot()
        self.timeline = TimelineChart()
        self.histogram = HistogramChart()
    def build_all(self):

        print(
            "Generando gráficas..."
        )

        # =====================================
        # INVENTARIO
        # =====================================

        self.bar.create(
            data=self.inventory.anexos_por_tipo_archivo(),
            category_col="tipo_archivo",
            value_col="total",
            title="Anexos por tipo de archivo",
            filename="anexos_por_tipo_archivo.png"
        )

        self.bar.create(
            data=self.inventory.documentos_por_reparto(),
            category_col="reparto",
            value_col="total",
            title="Documentos por reparto",
            filename="documentos_por_reparto.png"
        )

        self.bar.create(
            data=self.inventory.documentos_por_magistrado(),
            category_col="magistrado_fiscal",
            value_col="total",
            title="Documentos por magistrado",
            filename="documentos_por_magistrado.png"
        )

        # =====================================
        # PIPELINE
        # =====================================

        self.bar.create(
            data=self.pipeline.status_extract_distribution(),
            category_col="status_extract",
            value_col="total",
            title="Estado de extracción",
            filename="status_extract.png"
        )

        self.bar.create(
            data=self.pipeline.status_solar_distribution(),
            category_col="status_solar",
            value_col="total",
            title="Estado Solar",
            filename="status_solar.png"
        )

        self.bar.create(
            data=self.pipeline.vector_distribution(),
            category_col="has_vector",
            value_col="total",
            title="Disponibilidad de vectores",
            filename="has_vector.png"
        )

        self.grouped.create(
            data=self.pipeline.extract_status_by_worker(),
            category_col="worker_host",
            fill_col="status_extract",
            value_col="total",
            title="Extracciones por worker",
            filename="extract_status_worker.png"
        )

        self.grouped.create(
            data=self.pipeline.solar_status_by_worker(),
            category_col="worker_host",
            fill_col="status_solar",
            value_col="total",
            title="Estado Solr por worker",
            filename="solar_status_worker.png"
        )

        # =====================================
        # INFRAESTRUCTURA
        # =====================================

        self.bar.create(
            data=self.infrastructure.worker_volume(),
            category_col="worker_host",
            value_col="total",
            title="Carga por worker",
            filename="worker_volume.png"
        )

        self.bar.create(
            data=self.infrastructure.worker_duration(),
            category_col="worker_host",
            value_col="avg_duration_seconds",
            title="Duración promedio por worker",
            filename="worker_duration.png"
        )

        self.bar.create(
            data=self.infrastructure.worker_cpu(),
            category_col="worker_host",
            value_col="avg_cpu_percent",
            title="CPU promedio por worker",
            filename="worker_cpu.png"
        )

        self.bar.create(
            data=self.infrastructure.worker_memory(),
            category_col="worker_host",
            value_col="avg_mem_mb",
            title="Memoria promedio por worker",
            filename="worker_memory.png"
        )

        # =====================================
        # TIMELINE
        # =====================================
        self.timeline.create(
            data=self.pipeline.processing_trend(),
            date_col="process_date",
            value_col="total",
            rolling_col="rolling_7d",
            title="Extracciones por día",
            filename="processing_trend.png"
        )

        # =====================================
        # HISTOGRAMAS
        # =====================================
        self.histogram.create(
            data=self.infrastructure.duration_distribution(),
            column="docling_duration_seconds",
            title="Distribución de duración de procesamiento",
            xlabel="Segundos",
            filename="duration_histogram.png"
        )

        self.histogram.create(
            data=self.infrastructure.cpu_distribution(),
            column="worker_cpu_percent",
            title="Distribución uso CPU",
            xlabel="CPU (%)",
            filename="cpu_histogram.png"
        )

        self.histogram.create(
            data=self.infrastructure.memory_distribution(),
            column="worker_mem_mb",
            title="Distribución uso memoria",
            xlabel="Memoria (MB)",
            filename="memory_histogram.png"
        )

        print(
            "Gráficas generadas."
        )