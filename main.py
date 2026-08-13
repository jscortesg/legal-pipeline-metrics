# main.py

from database.connection import DatabaseConnection
from database.queries import MetricsQueries

from stats.inventory import InventoryMetrics
from stats.pipeline import PipelineMetrics
from stats.infrastructure import InfrastructureMetrics

from visualize.dashboard import DashboardCharts


def main():

    db = DatabaseConnection()

    queries = MetricsQueries(db)

    inventory = InventoryMetrics(
        queries
    )

    pipeline = PipelineMetrics(
        queries
    )

    infrastructure = InfrastructureMetrics(
        queries
    )

    print(
        pipeline.extract_status_by_worker()
    )

    print(
        pipeline.solar_status_by_worker()
    )


if __name__ == "__main__":
    main()