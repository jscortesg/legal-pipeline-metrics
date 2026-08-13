# visualize/dashboard.py

from visualize.bar import BarPlot


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

        print(
            "Gráficas generadas."
        )