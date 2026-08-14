from database.connection import DatabaseConnection
from database.queries import MetricsQueries

from stats.inventory import InventoryMetrics
from stats.infrastructure import InfrastructureMetrics

from stats.pipeline import PipelineMetrics
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

    df = pipeline.processing_trend()

    print(df)

    print(
        "\nFilas:",
        len(df)
    )

    print(df.head(10))
    print(df.tail(10))

    dashboard = DashboardCharts(
        inventory=inventory,
        pipeline=pipeline,
        infrastructure=infrastructure
    )

    dashboard.build_all()


if __name__ == "__main__":
    main()