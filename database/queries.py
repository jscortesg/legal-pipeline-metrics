# database/queries.py

import polars as pl


class MetricsQueries:

    def __init__(self, connection):

        self.connection = connection

    def count_rows(
        self,
        table_name: str
    ) -> int:

        query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        """

        with self.connection.connect() as conn:

            with conn.cursor() as cur:

                cur.execute(query)

                return cur.fetchone()[0]

    def total_expedientes(self) -> int:

        return self.count_rows(
            "expediente"
        )

    def total_cuadernos(self) -> int:

        return self.count_rows(
            "cuaderno"
        )

    def total_documentos(self) -> int:

        return self.count_rows(
            "documento"
        )

    def total_anexos(self) -> int:

        return self.count_rows(
            "anexo"
        )

    def total_inventarios(self) -> int:

        return self.count_rows(
            "inventario_jerarquia"
        )

    def total_extracciones(self) -> int:

        return self.count_rows(
            "extraccion_corpus"
        )

    def anexos_por_tipo_archivo(self) -> pl.DataFrame:

        query = """
        SELECT
            tipo_archivo,
            COUNT(*) AS total
        FROM anexo
        GROUP BY tipo_archivo
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def documentos_por_reparto(self) -> pl.DataFrame:

        query = """
        SELECT
            reparto,
            COUNT(*) AS total
        FROM documento
        GROUP BY reparto
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def documentos_por_magistrado(self) -> pl.DataFrame:

        query = """
        SELECT
            magistrado_fiscal,
            COUNT(*) AS total
        FROM documento
        GROUP BY magistrado_fiscal
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def status_extract_distribution(self) -> pl.DataFrame:

        query = """
        SELECT
            status_extract,
            COUNT(*) AS total
        FROM extraccion_corpus
        GROUP BY status_extract
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def status_solar_distribution(self) -> pl.DataFrame:

        query = """
        SELECT
            status_solar,
            COUNT(*) AS total
        FROM extraccion_corpus
        GROUP BY status_solar
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def vector_distribution(self) -> pl.DataFrame:

        query = """
        SELECT
            has_vector,
            COUNT(*) AS total
        FROM extraccion_corpus
        GROUP BY has_vector
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def worker_volume(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            COUNT(*) AS total
        FROM extraccion_corpus
        WHERE status_extract <> 'PENDING'
        GROUP BY worker_host
        ORDER BY total DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def worker_duration(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            ROUND(
                AVG(docling_duration_seconds),
                2
            ) AS avg_duration_seconds
        FROM extraccion_corpus
        WHERE status_extract <> 'PENDING'
        GROUP BY worker_host
        ORDER BY avg_duration_seconds DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def worker_cpu(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            ROUND(
                AVG(worker_cpu_percent),
                2
            ) AS avg_cpu_percent
        FROM extraccion_corpus
        WHERE status_extract <> 'PENDING'
        GROUP BY worker_host
        ORDER BY avg_cpu_percent DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def worker_memory(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            ROUND(
                AVG(worker_mem_mb),
                2
            ) AS avg_mem_mb
        FROM extraccion_corpus
        WHERE status_extract <> 'PENDING'
        GROUP BY worker_host
        ORDER BY avg_mem_mb DESC
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )


    def extract_status_by_worker(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            status_extract,
            COUNT(*) AS total
        FROM extraccion_corpus
        GROUP BY
            worker_host,
            status_extract
        ORDER BY
            worker_host,
            status_extract
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )

    def solar_status_by_worker(self) -> pl.DataFrame:

        query = """
        SELECT
            worker_host,
            status_solar,
            COUNT(*) AS total
        FROM extraccion_corpus
        GROUP BY
            worker_host,
            status_solar
        ORDER BY
            worker_host,
            status_solar
        """

        with self.connection.connect() as conn:

            return pl.read_database(
                query=query,
                connection=conn
            )