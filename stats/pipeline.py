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

    def _trend(
        self,
        filter_expr: pl.Expr | None = None
    ) -> pl.DataFrame:

        df = self.extraccion

        if filter_expr is not None:
            df = df.filter(filter_expr)

        return (
            df
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

    def _trend_by_worker(
        self,
        status_filter: str | None = None
    ) -> pl.DataFrame:

        df = self.extraccion

        if status_filter is not None:
            df = df.filter(
                pl.col("worker_status") == status_filter
            )

        return (
            df
            .filter(
                pl.col("date_process").is_not_null()
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
            .group_by(
                [
                    "worker_host",
                    "process_date"
                ]
            )
            .len()
            .rename({"len": "total"})
            .sort(
                [
                    "worker_host",
                    "process_date"
                ]
            )
            .with_columns(
                pl.col("total")
                .rolling_mean(
                    window_size=7,
                    min_samples=1
                )
                .over("worker_host")
                .alias("rolling_7d")
            )
        )

    def status_extract_distribution(
        self
    ) -> pl.DataFrame:

        return self._distribution(
            "worker_status"
        )

    def status_solar_distribution(
        self
    ) -> pl.DataFrame:

        return self._distribution(
            "status_original"
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
            "worker_status"
        )

    def solar_status_by_worker(
        self
    ) -> pl.DataFrame:

        return self._worker_distribution(
            "status_original"
        )

    def processing_trend(
        self
    ) -> pl.DataFrame:

        return self._trend()


    def extract_success_trend(
        self
    ) -> pl.DataFrame:

        return self._trend(
            pl.col("worker_status") == "done"
        )


    def extract_failed_trend(
        self
    ) -> pl.DataFrame:

        return self._trend(
            pl.col("worker_status") == "error"
        )


    def vectorized_trend(
        self
    ) -> pl.DataFrame:

        return self._trend(
            pl.col("has_vector")
        )

    def processing_trend_by_worker(
        self
    ) -> pl.DataFrame:

        return self._trend_by_worker()


    def success_trend_by_worker(
        self
    ) -> pl.DataFrame:

        return self._trend_by_worker(
            "done"
        )


    def failed_trend_by_worker(
        self
    ) -> pl.DataFrame:

        return self._trend_by_worker(
            "error"
        )