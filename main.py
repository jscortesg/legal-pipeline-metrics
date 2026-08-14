from database.connection import DatabaseConnection
from database.queries import DatasetQueries

from stats.pipeline import PipelineMetrics


def main():

    db = DatabaseConnection()

    loader = DatasetQueries(db)

    dfs = loader.load_all()

    pipeline = PipelineMetrics(dfs)

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


if __name__ == "__main__":
    main()