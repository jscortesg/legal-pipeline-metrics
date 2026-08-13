from stats.base import MetricsDataset


class PipelineMetrics(MetricsDataset):

    def status_extract_distribution(self):

        return self.queries.status_extract_distribution()

    def status_solar_distribution(self):

        return self.queries.status_solar_distribution()

    def vector_distribution(self):

        return self.queries.vector_distribution()