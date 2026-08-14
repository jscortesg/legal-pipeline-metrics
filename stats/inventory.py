# stats/inventory.py

import polars as pl

from stats.base import MetricsDataset


class InventoryMetrics(MetricsDataset):

    def summary(self):

        return {
            "expedientes":
                self.expediente.height,

            "cuadernos":
                self.cuaderno.height,

            "documentos":
                self.documento.height,

            "anexos":
                self.anexo.height,

            "inventarios":
                self.inventario.height,

            "extracciones":
                self.extraccion.height
        }

    def _distribution(
        self,
        df: pl.DataFrame,
        column: str
    ) -> pl.DataFrame:

        return (
            df
            .group_by(column)
            .len()
            .rename({"len": "total"})
            .sort(
                "total",
                descending=True
            )
        )

    def anexos_por_tipo_archivo(self):

        return self._distribution(
            self.anexo,
            "tipo_archivo"
        )

    def documentos_por_reparto(self):

        return self._distribution(
            self.documento,
            "reparto"
        )

    def documentos_por_magistrado(self):

        return self._distribution(
            self.documento,
            "magistrado_fiscal"
        )