# database/queries.py

import polars as pl


class DatasetQueries:

    TABLES = [
        "anexo",
        "auditoria_generacion",
        "cuaderno",
        "documento",
        "expediente",
        "extraccion_corpus",
        "inventario_jerarquia"
    ]

    def __init__(self, connection):

        self.connection = connection

    def load_table(
        self,
        table_name: str
    ) -> pl.DataFrame:

        with self.connection.connect() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        column_name,
                        data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                    """,
                    (table_name,)
                )

                columns = cur.fetchall()

            select_columns = []

            for column_name, data_type in columns:

                if data_type in (
                    "date",
                    "timestamp without time zone",
                    "timestamp with time zone"
                ):

                    select_columns.append(
                        f"{column_name}::text AS {column_name}"
                    )

                else:

                    select_columns.append(
                        column_name
                    )

            query = f"""
            SELECT
                {", ".join(select_columns)}
            FROM {table_name}
            """

            return pl.read_database(
                query=query,
                connection=conn
            )

    def load_all(self):

        return {
            table: self.load_table(table)
            for table in self.TABLES
        }