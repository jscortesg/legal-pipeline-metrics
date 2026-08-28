from plotnine import (
    ggplot,
    aes,
    geom_line,
    labs,
    theme_minimal,
    theme,
    element_text,
    scale_x_datetime
)

from visualize.base import BasePlot


class WorkerTimelineChart(BasePlot):

    def create(
        self,
        data,
        title: str,
        filename: str
    ):

        pdf = data.to_pandas()

        pdf = pdf[
            pdf["rolling_7d"].notna()
        ]

        plot = (
            ggplot(
                pdf,
                aes(
                    x="process_date",
                    y="rolling_7d",
                    color="worker_host"
                )
            )
            + geom_line(size=1.1)
            + labs(
                title=title,
                x="Fecha",
                y="Promedio móvil (7 días)",
                color="Worker"
            )
            + scale_x_datetime(
                date_breaks="1 month",
                date_labels="%Y-%m"
            )
            + theme_minimal()
            + theme(
                axis_text_x=element_text(
                    rotation=45,
                    ha="right"
                ),
                legend_position="right"
            )
        )

        self.save(
            plot,
            filename
        )