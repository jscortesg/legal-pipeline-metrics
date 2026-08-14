from database.connection import DatabaseConnection
from database.queries import DatasetQueries

from stats.pipeline import PipelineMetrics
from stats.inventory import InventoryMetrics
from stats.infrastructure import InfrastructureMetrics


def main():

    db = DatabaseConnection()

    loader = DatasetQueries(db)

    dfs = loader.load_all()

    pipeline = PipelineMetrics(dfs)
    inventory = InventoryMetrics(dfs)
    infrastructure = InfrastructureMetrics(dfs)

    print(
        pipeline.status_extract_distribution()
    )

    print(pipeline.status_solar_distribution())
    print()
    print(pipeline.vector_distribution())
    print()
    print(pipeline.extract_status_by_worker())
    print()
    print(pipeline.solar_status_by_worker())

    print(
        pipeline.processing_trend()
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

    print(
    infrastructure.worker_volume()
    )

    print(
        infrastructure.worker_duration()
    )

    print(
        infrastructure.worker_cpu()
    )

    print(
        infrastructure.worker_memory()
    )

    print(
        infrastructure.duration_distribution().head()
    )

    print(
        infrastructure.cpu_distribution().head()
    )

    print(
        infrastructure.memory_distribution().head()
    )


if __name__ == "__main__":
    main()