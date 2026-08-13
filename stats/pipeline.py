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