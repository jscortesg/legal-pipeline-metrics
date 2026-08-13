# stats/infrastructure.py

from stats.base import MetricsDataset


class InfrastructureMetrics(MetricsDataset):

    def worker_volume(self):

        return self.queries.worker_volume()

    def worker_duration(self):

        return self.queries.worker_duration()

    def worker_cpu(self):

        return self.queries.worker_cpu()

    def worker_memory(self):

        return self.queries.worker_memory()