# visualize/bar.py

from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_text,
    theme_minimal,
    labs,
    theme,
    element_text,
    scale_fill_manual
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

        plot = (
            ggplot(
                data.to_pandas()
            )
            + aes(
                x=category_col,
                y=value_col,
                fill=category_col
            )
            + geom_col()
            + geom_text(
                aes(label=value_col),
                va="bottom"
            )
            + labs(
                title=title,
                x="",
                y="Cantidad"
            )
            + scale_fill_manual(
                values=[
                    "#4E79A7",
                    "#F28E2B",
                    "#59A14F",
                    "#E15759",
                    "#76B7B2",
                    "#EDC948"
                ]
            )
            + theme_minimal()
            + theme(
                axis_text_x=element_text(
                    rotation=45,
                    ha="right"
                ),
                figure_size=(8, 5)
            )
        )

        self.save(
            plot,
            filename
        )