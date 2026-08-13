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

    dashboard = DashboardCharts(
        inventory=inventory,
        pipeline=pipeline,
        infrastructure=infrastructure
    )

    dashboard.build_all()


if __name__ == "__main__":
    main()