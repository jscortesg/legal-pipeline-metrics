# stats/base.py

from database.queries import MetricsQueries


class MetricsDataset:

    def __init__(
        self,
        queries: MetricsQueries
    ):
        self.queries = queries