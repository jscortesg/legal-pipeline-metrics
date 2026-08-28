import polars as pl

from stats.pipeline import PipelineMetrics

TEST_DATES = [
    "2026-01-01",
    "2026-01-02",
    "2026-01-03",
    "2026-01-04",
    "2026-01-05",
    "2026-01-06",
    "2026-01-07",
    "2026-01-08",
]

def build_metrics(extraccion_df):

    return PipelineMetrics(
        {
            "extraccion_corpus": extraccion_df,
            "documento": pl.DataFrame(),
            "anexo": pl.DataFrame(),
            "inventario_jerarquia": pl.DataFrame(),
            "cuaderno": pl.DataFrame(),
            "expediente": pl.DataFrame(),
            "auditoria_generacion": pl.DataFrame(),
        }
    )


def test_status_extract_distribution():

    df = pl.DataFrame(
        {
            "worker_status": [
                "SUCCESS",
                "SUCCESS",
                "FAILED"
            ]
        }
    )

    metrics = build_metrics(df)

    result = (
        metrics
        .status_extract_distribution()
        .sort("worker_status")
    )

    assert result.height == 2

    expected = {
        "FAILED": 1,
        "SUCCESS": 2
    }

    for row in result.to_dicts():
        assert row["total"] == expected[row["worker_status"]]

def test_status_solar_distribution():

    df = pl.DataFrame(
        {
            "status_original": [
                True,
                True,
                False
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.status_solar_distribution()

    result_dict = {
        row["status_original"]: row["total"]
        for row in result.to_dicts()
    }

    assert result_dict == {
        True: 2,
        False: 1
    }


def test_vector_distribution():

    df = pl.DataFrame(
        {
            "has_vector": [
                True,
                True,
                False
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.vector_distribution()

    result_dict = {
        row["has_vector"]: row["total"]
        for row in result.to_dicts()
    }

    assert result_dict == {
        True: 2,
        False: 1
    }


def test_extract_status_by_worker():

    df = pl.DataFrame(
        {
            "worker_host": [
                "worker-01",
                "worker-01",
                "worker-02"
            ],
            "worker_status": [
                "SUCCESS",
                "FAILED",
                "SUCCESS"
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.extract_status_by_worker()

    assert result["total"].sum() == 3


def test_processing_trend():

    df = pl.DataFrame(
        {
            "date_process": TEST_DATES
        }
    )

    metrics = build_metrics(df)

    result = metrics.processing_trend()

    assert result["total"].sum() == 8

    assert "process_date" in result.columns
    assert "rolling_7d" in result.columns

    assert result["rolling_7d"].is_not_null().all()
    assert result["rolling_7d"].len() > 0
    assert result.height == 8


def test_extract_success_trend():

    df = pl.DataFrame(
        {
            "date_process": TEST_DATES,
            "worker_status": [
                "done",
                "error",
                "done",
                "done",
                "error",
                "done",
                "done",
                "error"
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.extract_success_trend()

    assert result["total"].sum() == 5

    assert "rolling_7d" in result.columns
    assert result["rolling_7d"].len() > 0


def test_extract_failed_trend():

    df = pl.DataFrame(
        {
            "date_process": TEST_DATES,
            "worker_status": [
                "done",
                "error",
                "error",
                "done",
                "error",
                "done",
                "error",
                "done"
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.extract_failed_trend()

    assert result["total"].sum() == 4

    assert "rolling_7d" in result.columns
    assert result["rolling_7d"].len() > 0


def test_vectorized_trend():

    df = pl.DataFrame(
        {
            "date_process": TEST_DATES,
            "has_vector": [
                True,
                False,
                True,
                True,
                False,
                True,
                True,
                False
            ]
        }
    )

    metrics = build_metrics(df)

    result = metrics.vectorized_trend()

    assert result["total"].sum() == 5


def test_processing_trend_by_worker():

    df = pl.DataFrame(
        {
            "worker_host": [
                "worker-01",
                "worker-01",
                "worker-01",
                "worker-02",
                "worker-02",
                "worker-02",
                "worker-03",
                "worker-03"
            ],
            "date_process": TEST_DATES
        }
    )

    metrics = build_metrics(df)

    result = metrics.processing_trend_by_worker()

    assert result["total"].sum() == 8

    assert "worker_host" in result.columns
    assert "rolling_7d" in result.columns
    assert result["rolling_7d"].len() > 0

    assert result["worker_host"].n_unique() == 3

    assert (
        set(result["worker_host"].unique().to_list())
        == {
            "worker-01",
            "worker-02",
            "worker-03"
        }
    )

    
