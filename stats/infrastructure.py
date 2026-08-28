# stats/infrastructure.py

import polars as pl

from stats.base import MetricsDataset


class InfrastructureMetrics(MetricsDataset):

    def _processed(self):

        return self.extraccion.filter(
            pl.col("worker_status") != "processing"
        )

    def _worker_metric(
        self,
        column: str,
        alias: str
    ) -> pl.DataFrame:

        return (
            self._processed()
            .group_by("worker_host")
            .agg(
                pl.col(column)
                .mean()
                .alias(alias)
            )
            .sort(
                alias,
                descending=True
            )
        )

    def worker_volume(self):

        return (
            self._processed()
            .group_by("worker_host")
            .len()
            .rename({"len": "total"})
            .sort(
                "total",
                descending=True
            )
        )

    def worker_duration(self):

        return self._worker_metric(
            "docling_duration_seconds",
            "avg_duration_seconds"
        )

    def worker_cpu(self):

        return self._worker_metric(
            "worker_cpu_percent",
            "avg_cpu_percent"
        )

    def worker_memory(self):

        return self._worker_metric(
            "worker_mem_mb",
            "avg_mem_mb"
        )

    def duration_distribution(self):

        return (
            self._processed()
            .select(
                "docling_duration_seconds"
            )
        )

    def cpu_distribution(self):

        return (
        self._processed()
        .select(
            "worker_cpu_percent"
        )
    )

    def memory_distribution(self):

        return (
        self._processed()
        .select(
            "worker_mem_mb"
        )
    )