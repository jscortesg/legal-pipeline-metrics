import polars as pl


class DatasetQueries:

    TABLES = [
        "ANEXO",
        "CUADERNO",
        "DOCUMENTO",
        "EXPEDIENTE",
        "EXTRACCION_CORPUS",
        "INVENTARIO_JERARQUIA",
        "_etl_runs",
        "_quarantine_fk",
        "_sync_state_v2"
    ]

    SAMPLE_SIZES = {
        "ANEXO": 10000,
        "CUADERNO": 10000,
        "DOCUMENTO": 10000,
        "EXPEDIENTE": 10000,
        "EXTRACCION_CORPUS": 10000,
        "INVENTARIO_JERARQUIA": 10000,
        "_etl_runs": 1000,
        "_quarantine_fk": 1000,
        "_sync_state_v2": 1000,
    }

    def __init__(self, connection):

        self.connection = connection

    def load_table(
        self,
        table_name: str,
        query: str | None = None
    ) -> pl.DataFrame:

        with self.connection.connect() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                        SELECT
                            column_name,
                            data_type
                        FROM information_schema.columns
                        WHERE table_schema = 'etl'
                        AND table_name = %s
                        ORDER BY ordinal_position
                    """,
                    (table_name,)
                )

                columns = cur.fetchall()

            if query is None:

                select_columns = []

                for column_name, data_type in columns:

                    column_identifier = f'"{column_name}"'

                    if data_type in (
                        "date",
                        "timestamp without time zone",
                        "timestamp with time zone"
                    ):

                        select_columns.append(
                            f"{column_identifier}::text AS {column_identifier}"
                        )

                    else:

                        select_columns.append(
                            column_identifier
        )

                if table_name == "EXTRACCION_CORPUS":

                    query = f"""
                        SELECT
                            {", ".join(select_columns)}
                        FROM etl."{table_name}"
                        TABLESAMPLE BERNOULLI (0.2)
                        ORDER BY random()
                        LIMIT {self.SAMPLE_SIZES[table_name]}
                    """

                else:

                    query = f"""
                        SELECT
                            {", ".join(select_columns)}
                        FROM etl."{table_name}"
                        LIMIT {self.SAMPLE_SIZES[table_name]}
                    """

            df = pl.read_database(
                query=query,
                connection=conn,
                infer_schema_length=None
            )

            df = df.rename({
                column: column.lower()
                for column in df.columns
            })

            return df

    def load_all(self):

        return {
            table.lower(): self.load_table(table)
            for table in self.TABLES
        }