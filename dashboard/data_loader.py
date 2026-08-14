from database.connection import DatabaseConnection
from database.queries import DatasetQueries

from stats.inventory import InventoryMetrics
from stats.pipeline import PipelineMetrics
from stats.infrastructure import InfrastructureMetrics

def load_metrics():

    connection = DatabaseConnection()

    dfs = DatasetQueries(
        connection
    ).load_all()

    return {
        "inventory": InventoryMetrics(dfs),
        "pipeline": PipelineMetrics(dfs),
        "infrastructure": InfrastructureMetrics(dfs)
    }