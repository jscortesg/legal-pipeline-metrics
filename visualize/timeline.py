from plotnine import (
    ggplot,
    aes,
    geom_line,
    geom_point,
    xlab,
    ylab,
    scale_color_manual,
    labs,
    theme,
    element_text,
    theme_minimal
)

import pandas as pd

from visualize.base import BasePlot


class TimelineChart(BasePlot):

    def create(
        self,
        data,
        date_col: str,
        value_col: str,
        rolling_col: str,
        title: str,
        filename: str
    ):

        pdf = data.to_pandas()

        daily = (
            pdf[
                [date_col, value_col]
            ]
            .rename(
                columns={
                    value_col: "value"
                }
            )
        )

        daily["serie"] = "Diario"

        rolling = (
            pdf[
                [date_col, rolling_col]
            ]
            .rename(
                columns={
                    rolling_col: "value"
                }
            )
        )

        rolling["serie"] = "Promedio móvil (7 días)"

        plot_df = pd.concat(
            [daily, rolling],
            ignore_index=True
        )

        plot = (
            ggplot(
                plot_df,
                aes(
                    x=date_col,
                    y="value",
                    color="serie"
                )
            )
            + geom_line(size=1.2)
            + geom_point(size=1)
            + scale_color_manual(
                values={
                    "Diario": "#B0B0B0",
                    "Promedio móvil (7 días)": "#1F77B4"
                }
            )
            + labs(
                title=title,
                color=""
            )
            + xlab("Fecha")
            + ylab("Documentos procesados")
            + theme_minimal()
            + theme(
                axis_text_x=element_text(
                    rotation=45,
                    ha="right"
                )
            )
        )

        self.save(
            plot,
            filename
        )