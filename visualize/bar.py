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
    scale_y_continuous
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

        total = (
            data
            .select(
                pl.col(value_col).sum()
            )
            .item()
        )

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

        missing_percentage = (
            missing_total * 100 / total
            if total
            else 0
        )

        plot_data = (
            data
            .filter(
                pl.col(category_col).is_not_null()
            )
        )

        max_value = (
            plot_data
            .select(
                pl.col(value_col).max()
            )
            .item()
        )

        category_count = plot_data.height

        plot_data = plot_data.to_pandas()

        plot = (
            ggplot(
                plot_data,
                aes(
                    x=category_col,
                    y=value_col,
                    fill=category_col
                )
            )
            + geom_col()
            + geom_text(
                aes(
                    label=value_col
                ),
                va="bottom"
            )
            + labs(
                title=title,
                x="",
                y="Cantidad"
            )
            + scale_y_continuous(
                limits=(
                    0,
                    max_value * 1.15
                )
            )
            + theme_minimal()
            + theme(
                axis_text_x=element_text(
                    rotation=45,
                    ha="right"
                ),
                legend_position="none"
            )
        )

        if missing_total > 0:

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

        self.save(
            plot,
            filename
        )