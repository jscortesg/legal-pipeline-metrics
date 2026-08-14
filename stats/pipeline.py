import polars as pl

from stats.base import MetricsDataset


class PipelineMetrics(MetricsDataset):

    def _distribution(
        self,
        column: str
    ) -> pl.DataFrame:

        return (
            self.extraccion
            .group_by(column)
            .len()
            .rename({"len": "total"})
            .sort(
                "total",
                descending=True
            )
        )

    def _worker_distribution(
        self,
        status_column: str
    ) -> pl.DataFrame:

        return (
            self.extraccion
            .group_by(
                [
                    "worker_host",
                    status_column
                ]
            )
            .len()
            .rename({"len": "total"})
            .sort(
                [
                    "worker_host",
                    status_column
                ]
            )
        )

    def status_extract_distribution(
        self
    ) -> pl.DataFrame:

        return self._distribution(
            "status_extract"
        )

    def status_solar_distribution(
        self
    ) -> pl.DataFrame:

        return self._distribution(
            "status_solar"
        )

    def vector_distribution(
        self
    ) -> pl.DataFrame:

        return self._distribution(
            "has_vector"
        )

    def extract_status_by_worker(
        self
    ) -> pl.DataFrame:

        return self._worker_distribution(
            "status_extract"
        )

    def solar_status_by_worker(
        self
    ) -> pl.DataFrame:

        return self._worker_distribution(
            "status_solar"
        )

    def processing_trend(
        self
    ) -> pl.DataFrame:

        return (
            self.extraccion
            .filter(
                pl.col("date_process").is_not_null()
            )
            .filter(
                pl.col("date_process")
                .str.slice(0, 4)
                .cast(
                    pl.Int32,
                    strict=False
                )
                < 2100
            )
            .with_columns(
                pl.col("date_process")
                .str.slice(0, 10)
                .str.strptime(
                    pl.Date,
                    "%Y-%m-%d",
                    strict=False
                )
                .alias("process_date")
            )
            .group_by("process_date")
            .len()
            .rename({"len": "total"})
            .sort("process_date")
            .with_columns(
                pl.col("total")
                .rolling_mean(
                    window_size=7,
                    min_samples=1
                )
                .alias("rolling_7d")
            )
        )