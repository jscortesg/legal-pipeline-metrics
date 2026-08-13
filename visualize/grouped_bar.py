from plotnine import (
    ggplot,
    aes,
    geom_col,
    labs,
    theme_minimal,
    theme,
    element_text,
    scale_fill_brewer
)

from visualize.base import BasePlot


class GroupedBarPlot(BasePlot):

    def create(
        self,
        data,
        category_col,
        fill_col,
        value_col,
        title,
        filename
    ):

        plot = (
            ggplot(
                data.to_pandas(),
                aes(
                    x=category_col,
                    y=value_col,
                    fill=fill_col
                )
            )
            + geom_col(
                position="dodge"
            )
            + scale_fill_brewer(
                type="qual",
                palette="Set2"
            )
            + labs(
                title=title,
                x="",
                y="Cantidad"
            )
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