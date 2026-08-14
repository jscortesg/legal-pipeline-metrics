from plotnine import (
    ggplot,
    aes,
    geom_histogram,
    labs,
    xlab,
    ylab,
    theme_minimal,
    theme,
    element_text,
    element_line
)

from visualize.base import BasePlot


class HistogramChart(BasePlot):

    def create(
        self,
        data,
        column,
        title,
        xlabel,
        filename,
        bins=20
    ):

        pdf = data.to_pandas()

        # Asegurar que la variable sea numérica
        pdf[column] = (
            pdf[column]
            .astype(float)
        )

        pdf = pdf.dropna(
            subset=[column]
        )

        plot = (

            ggplot(
                pdf,
                aes(x=column)
            )

            + geom_histogram(
                bins=bins,
                fill="#5B8CC0",
                color="#2B2B2B",
                size=0.5,
                alpha=0.85
            )

            + labs(
                title=title
            )

            + xlab(xlabel)
            + ylab("Frecuencia")

            + theme_minimal()

            + theme(

                figure_size=(9, 5.5),

                plot_title=element_text(
                    size=15,
                    weight="bold"
                ),

                axis_title=element_text(
                    size=11
                ),

                axis_text_x=element_text(
                    size=9
                ),

                axis_text_y=element_text(
                    size=9
                ),

                axis_line=element_line(
                    color="black",
                    size=0.7
                )
            )
        )

        self.save(
            plot,
            filename
        )