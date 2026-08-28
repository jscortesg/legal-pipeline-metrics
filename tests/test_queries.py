import unittest
from unittest.mock import MagicMock, patch

import polars as pl

from database.queries import DatasetQueries


class TestDatasetQueries(unittest.TestCase):

    def test_tables_are_defined_in_uppercase(self):
        expected = [
            "ANEXO",
            "CUADERNO",
            "DOCUMENTO",
            "EXPEDIENTE",
            "EXTRACCION_CORPUS",
            "INVENTARIO_JERARQUIA",
            "_etl_runs",
            "_quarantine_fk",
            "_sync_state_v2",
        ]

        self.assertEqual(
            DatasetQueries.TABLES,
            expected
        )

    def test_load_table_uses_etl_schema_and_quoted_identifiers(self):
        connection = MagicMock()
        conn = MagicMock()
        cursor = MagicMock()

        connection.connect.return_value.__enter__.return_value = conn
        conn.cursor.return_value.__enter__.return_value = cursor

        cursor.fetchall.return_value = [
            ("EXP_NUMERO", "character varying"),
            ("ASUNTO", "text"),
            ("UPDATED_AT", "timestamp without time zone"),
        ]

        df = pl.DataFrame({
            "EXP_NUMERO": ["001"],
            "ASUNTO": ["Prueba"],
            "UPDATED_AT": ["2026-08-27 10:00:00"],
        })

        with patch(
            "database.queries.pl.read_database",
            return_value=df
        ) as read_database:

            queries = DatasetQueries(connection)
            result = queries.load_table("EXPEDIENTE")

        metadata_query = cursor.execute.call_args_list[0].args[0]

        self.assertIn(
            "table_schema = 'etl'",
            metadata_query
        )

        self.assertEqual(
            cursor.execute.call_args_list[0].args[1],
            ("EXPEDIENTE",)
        )

        data_query = read_database.call_args.kwargs["query"]

        self.assertIn(
            'FROM etl."EXPEDIENTE"',
            data_query
        )

        self.assertIn(
            '"EXP_NUMERO"',
            data_query
        )

        self.assertIn(
            '"ASUNTO"',
            data_query
        )

        self.assertIn(
            '"UPDATED_AT"',
            data_query
        )

        self.assertEqual(
            result.columns,
            [
                "exp_numero",
                "asunto",
                "updated_at",
            ]
        )

    def test_load_all_returns_lowercase_keys(self):
        connection = MagicMock()
        queries = DatasetQueries(connection)

        with patch.object(
            queries,
            "load_table",
            side_effect=lambda table: pl.DataFrame({
                "dummy": [table]
            })
        ):

            result = queries.load_all()

        expected_keys = {
            "anexo",
            "cuaderno",
            "documento",
            "expediente",
            "extraccion_corpus",
            "inventario_jerarquia",
            "_etl_runs",
            "_quarantine_fk",
            "_sync_state_v2",
        }

        self.assertEqual(
            set(result.keys()),
            expected_keys
        )

        self.assertEqual(
            result["expediente"]["dummy"].to_list(),
            ["EXPEDIENTE"]
        )

    def test_load_table_converts_column_names_to_lowercase(self):
        connection = MagicMock()
        conn = MagicMock()
        cursor = MagicMock()

        connection.connect.return_value.__enter__.return_value = conn
        conn.cursor.return_value.__enter__.return_value = cursor

        cursor.fetchall.return_value = [
            ("MAGISTRADO_FISCAL", "text"),
            ("DOC_ID", "bigint"),
        ]

        df = pl.DataFrame({
            "MAGISTRADO_FISCAL": ["MAGISTRADO A"],
            "DOC_ID": [123],
        })

        with patch(
            "database.queries.pl.read_database",
            return_value=df
        ):

            queries = DatasetQueries(connection)
            result = queries.load_table("DOCUMENTO")

        self.assertEqual(
            result.columns,
            [
                "magistrado_fiscal",
                "doc_id",
            ]
        )


if __name__ == "__main__":
    unittest.main()
