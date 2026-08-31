# visualize/bar.py

import polars as pl
from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_text,
    geom_label,
    labs,
    theme_minimal,
    theme,
    element_text,
    scale_y_continuous,
    coord_flip
)

from visualize.base import BasePlot


class BarPlot(BasePlot):

    def create(
        self,
        data,
        category_col: str,
        value_col: str,
        title: str,
        filename: str
    ):

        # ============================================================
        # 1. Totales y datos faltantes
        # ============================================================

        total = (
            data
            .select(
                pl.col(value_col).sum()
            )
            .item()
        )

        total = total or 0

        missing_total = (
            data
            .filter(
                pl.col(category_col).is_null()
            )
            .select(
                pl.col(value_col).sum()
            )
            .item()
        )

        missing_total = missing_total or 0

        missing_percentage = (
            missing_total * 100 / total
            if total
            else 0
        )

        # ============================================================
        # 2. Datos que sí tienen categoría
        # ============================================================

        plot_data = (
            data
            .filter(
                pl.col(category_col).is_not_null()
            )
        )

        if plot_data.is_empty():
            return

        max_value = (
            plot_data
            .select(
                pl.col(value_col).max()
            )
            .item()
        )

        max_value = max_value or 0

        category_count = plot_data.height

        # ============================================================
        # 3. Formato de las etiquetas numéricas
        # ============================================================

        def format_value(value):

            if value is None:
                return ""

            if isinstance(value, float):

                if value.is_integer():
                    return f"{int(value):,}"

                return f"{value:,.2f}"

            return f"{value:,}"

        plot_data = plot_data.with_columns(
            pl.col(value_col)
            .map_elements(
                format_value,
                return_dtype=pl.String
            )
            .alias("_label")
        )

        label_threshold = max_value * 0.01

        plot_data = plot_data.with_columns(
            pl.when(
                pl.col(value_col) >= label_threshold
            )
            .then(
                pl.col("_label")
            )
            .otherwise(
                pl.lit("")
            )
            .alias("_plot_label")
        )

        # ============================================================
        # 4. Decidir orientación y tamaño
        # ============================================================

        # Con muchas categorías las barras horizontales son mucho
        # más legibles, especialmente para nombres largos.
        horizontal = category_count >= 10

        if horizontal:

            figure_width = 11

            # Una altura proporcional al número de categorías,
            # con un mínimo razonable.
            figure_height = max(
                8,
                category_count * 0.48
            )

        else:

            # Para pocas categorías mantenemos una gráfica
            # horizontalmente compacta.
            figure_width = max(
                9,
                category_count * 1.25
            )

            figure_height = 7

        # Espacio superior para las etiquetas numéricas.
        y_limit = (
            max_value * 1.15
            if max_value > 0
            else 1
        )

        # ============================================================
        # 5. Gráfica
        # ============================================================

        def shorten_category(value, max_length=35):

            if value is None:
                return ""

            value = str(value)

            if len(value) <= max_length:
                return value

            start = 20
            end = max_length - start - 1

            return (
                value[:start]
                + "…"
                + value[-end:]
            )


        plot_data = plot_data.with_columns(
            pl.col(category_col)
            .map_elements(
                shorten_category,
                return_dtype=pl.String
            )
            .alias("_category_label")
        )

        plot = (
            ggplot(
                plot_data.to_pandas(),
                aes(
                    x="_category_label",
                    y=value_col,
                    fill=category_col
                )
            )
            + geom_col()
            + geom_text(
                aes(
                    label="_plot_label"
                ),
                ha="left",
                va="center",
                nudge_y=max_value * 0.012
                if max_value > 0
                else 0.01,
                size=9
            )
            + labs(
                title=title,
                x="",
                y="Cantidad"
            )
            + scale_y_continuous(
                limits=(
                    0,
                    y_limit
                )
            )
            + theme_minimal()
            + theme(
                figure_size=(
                    figure_width,
                    figure_height
                ),
                axis_text_x=element_text(
                    rotation=45,
                    ha="right",
                    size=10
                ),
                axis_text_y=element_text(
                    size=10
                ),
                plot_title=element_text(
                    size=18
                ),
                legend_position="none"
            )
        )

        # ============================================================
        # 6. Orientación horizontal para muchas categorías
        # ============================================================

        if horizontal:

            plot = (
                plot
                + coord_flip()
                + theme(
                    axis_text_y=element_text(
                        size=9
                    ),
                    axis_text_x=element_text(
                        size=10
                    )
                )
            )

        # ============================================================
        # 7. Indicador de datos faltantes
        # ============================================================

        if missing_total > 0:

            if horizontal:

                plot = plot + geom_label(
                    aes(
                        x=category_count * 0.5,
                        y=max_value * 1.08
                    ),
                    label=(
                        f"Sin dato: {missing_total:,} "
                        f"({missing_percentage:.2f} %)"
                    ),
                    inherit_aes=False,
                    ha="center",
                    va="center"
                )

            else:

                plot = plot + geom_label(
                    aes(
                        x=category_count - 0.35,
                        y=max_value * 1.08
                    ),
                    label=(
                        f"Sin dato: {missing_total:,} "
                        f"({missing_percentage:.2f} %)"
                    ),
                    inherit_aes=False,
                    ha="right",
                    va="center"
                )

        # ============================================================
        # 8. Guardar
        # ============================================================

        self.save(
            plot,
            filename
        )