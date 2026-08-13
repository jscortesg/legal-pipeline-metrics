# stats/inventory.py

from stats.base import MetricsDataset


class InventoryMetrics(MetricsDataset):

    def summary(self):

        return {
            "expedientes":
                self.queries.total_expedientes(),

            "cuadernos":
                self.queries.total_cuadernos(),

            "documentos":
                self.queries.total_documentos(),

            "anexos":
                self.queries.total_anexos(),

            "inventarios":
                self.queries.total_inventarios(),

            "extracciones":
                self.queries.total_extracciones()
        }

    def anexos_por_tipo_archivo(self):

        return self.queries.anexos_por_tipo_archivo()

    def documentos_por_reparto(self):

        return self.queries.documentos_por_reparto()

    def documentos_por_magistrado(self):

        return self.queries.documentos_por_magistrado()