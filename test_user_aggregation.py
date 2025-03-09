# test_user_aggregation.py
import pytest
from pyspark.sql import SparkSession
from user_aggregation import read_data, filter_data, aggregate_state_data

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder \
        .appName("user_aggregation_test") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_data(spark):
    data = [
        {"user_id": 1, "geo": "US", "date": "2025-03-09", "state": "CA", "age": 25, "purchase_amount": 100.0},
        {"user_id": 2, "geo": "US", "date": "2025-03-09", "state": "NY", "age": 30, "purchase_amount": 150.0},
        {"user_id": 3, "geo": "US", "date": "2025-03-09", "state": "CA", "age": 35, "purchase_amount": 200.0},
        {"user_id": 4, "geo": "US", "date": "2025-03-08", "state": "CA", "age": 40, "purchase_amount": 250.0},
        {"user_id": 5, "geo": "CA", "date": "2025-03-09", "state": "ON", "age": 45, "purchase_amount": 300.0}
    ]
    return spark.createDataFrame(data)

def test_filter_data(sample_data):
    filtered_df = filter_data(sample_data, "US", "2025-03-09")
    assert filtered_df.count() == 3

def test_aggregate_state_data(sample_data):
    filtered_df = filter_data(sample_data, "US", "2025-03-09")
    result_df = aggregate_state_data(filtered_df).collect()

    assert len(result_df) == 2
    ca_data = next(row for row in result_df if row.state == "CA")
    assert ca_data.user_count == 2
    assert ca_data.avg_age == 30
    assert ca_data.median_age == 30
    assert ca_data.total_revenue == 300.0
    assert ca_data.avg_purchase_per_user == 150.0
    assert ca_data.user_count_rank == 1
