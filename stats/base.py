# stats/base.py

import polars as pl


class MetricsDataset:

    def __init__(self, dfs):

        self.dfs = dfs

        self.extraccion = dfs["extraccion_corpus"]
        self.documento = dfs["documento"]
        self.anexo = dfs["anexo"]
        self.inventario = dfs["inventario_jerarquia"]

        # opcionales
        self.cuaderno = dfs["cuaderno"]
        self.expediente = dfs["expediente"]
        self.auditoria = dfs["auditoria_generacion"]