from database.connection import DatabaseConnection
from database.queries import MetricsQueries
from stats.inventory import InventoryMetrics
from stats.pipeline import PipelineMetrics
from stats.infrastructure import (
    InfrastructureMetrics
)


def main():

    db = DatabaseConnection()

    queries = MetricsQueries(db)

    inventory = InventoryMetrics(
        queries
    )

    infra = InfrastructureMetrics(
        queries
    )

    print(
    inventory.summary()
    )

    print(
    inventory.anexos_por_tipo_archivo()
    )

    print(
        inventory.documentos_por_reparto()
    )

    print(
        inventory.documentos_por_magistrado()
    )

    pipeline = PipelineMetrics(
        queries
    )

    print(
        pipeline.status_extract_distribution()
    )

    print(
        pipeline.status_solar_distribution()
    )

    print(
        pipeline.vector_distribution()
    )

    print(
        infra.worker_volume()
    )

    print(
        infra.worker_duration()
    )

    print(
        infra.worker_cpu()
    )

    print(
        infra.worker_memory()
    )


if __name__ == "__main__":
    main()