import polars as pl

from stats.inventory import InventoryMetrics

def build_inventory_metrics(
    documento_df=None,
    anexo_df=None,
    inventario_df=None
):

    return InventoryMetrics(
        {
            "extraccion_corpus": pl.DataFrame(),
            "documento": (
                documento_df
                if documento_df is not None
                else pl.DataFrame()
            ),
            "anexo": (
                anexo_df
                if anexo_df is not None
                else pl.DataFrame()
            ),
            "inventario_jerarquia": (
                inventario_df
                if inventario_df is not None
                else pl.DataFrame()
            ),
            "cuaderno": pl.DataFrame(),
            "expediente": pl.DataFrame(),
        }
    )


def test_anexos_por_tipo_archivo_conserva_total():

    df = pl.DataFrame(
        {
            "tipo_archivo": [
                "pdf",
                "pdf",
                "docx",
                "xlsx"
            ]
        }
    )

    metrics = build_inventory_metrics(
        anexo_df=df
    )   

    result = metrics.anexos_por_tipo_archivo()

    assert result["total"].sum() == df.height