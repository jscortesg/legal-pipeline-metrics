import polars as pl

from stats.base import MetricsDataset


class PipelineMetrics(MetricsDataset):

    def status_extract_distribution(self):

        return self.queries.status_extract_distribution()

    def status_solar_distribution(self):

        return self.queries.status_solar_distribution()

    def vector_distribution(self):

        return self.queries.vector_distribution()

    def extract_status_by_worker(self):

        return self.queries.extract_status_by_worker()

    def solar_status_by_worker(self):

        return self.queries.solar_status_by_worker()

    def processing_trend(self):

        df = self.queries.processing_trend()

        return (
            df
            .with_columns(
                pl.col("total")
                .rolling_mean(
                    window_size=7,
                    min_periods=1
                )
                .alias("rolling_7d")
            )
        )