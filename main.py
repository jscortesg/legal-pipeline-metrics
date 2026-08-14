from database.connection import DatabaseConnection
from database.queries import DatasetQueries


def main():

    db = DatabaseConnection()

    queries = DatasetQueries(db)

    dfs = queries.load_all()

    print("\nTablas cargadas:")
    print("-" * 50)

    for table_name, df in dfs.items():

        print(
            f"{table_name}: "
            f"{df.height} filas x "
            f"{df.width} columnas"
        )

    print("\nColumnas de EXTRACCION_CORPUS:")
    print("-" * 50)

    print(
        dfs["extraccion_corpus"].columns
    )

    print("\nPrimeras filas:")
    print("-" * 50)

    print(
        dfs["extraccion_corpus"].head()
    )


if __name__ == "__main__":
    main()