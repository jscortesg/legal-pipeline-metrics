# stats/inventory.py

import polars as pl

from stats.base import MetricsDataset


class InventoryMetrics(MetricsDataset):

    def _filtrar_documentos(
        self,
        magistrado: str | None = None
    ) -> pl.DataFrame:

        if magistrado is None:
            return self.documento

        return self.documento.filter(
            pl.col("magistrado_fiscal") == magistrado
        )

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

    def anexos_por_tipo_archivo(
        self,
        magistrado_fiscal: str | None = None
    ):

        df = self.anexo

        if magistrado_fiscal is not None:

            df = (
                df.join(
                    self.documento.select(
                        [
                            "doc_id",
                            "magistrado_fiscal"
                        ]
                    ),
                    on="doc_id",
                    how="inner"
                )
                .filter(
                    pl.col("magistrado_fiscal")
                    == magistrado_fiscal
                )
            )

        return self._distribution(
            df,
            "tipo_archivo"
        )

    def documentos_por_reparto(
        self,
        magistrado=None
    ):

        return self._distribution(
            self._filtrar_documentos(magistrado),
            "reparto"
        )

    def documentos_por_magistrado(
        self,
        magistrado=None
    ):

        return self._distribution(
            self._filtrar_documentos(magistrado),
            "magistrado_fiscal"
        )