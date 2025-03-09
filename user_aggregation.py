# user_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, rank, percentile_approx
from pyspark.sql.window import Window

def read_data(spark, input_path):
    return spark.read.parquet(input_path)

def filter_data(df, geo, date):
    return df.filter((col("geo") == geo) & (col("date") == date))

def aggregate_state_data(df_filtered):
    state_aggs = df_filtered.groupBy("date", "state").agg(
        count("user_id").alias("user_count"),
        avg("age").alias("avg_age"),
        percentile_approx("age", 0.5).alias("median_age"),
        sum("purchase_amount").alias("total_revenue"),
        (sum("purchase_amount") / count("user_id")).alias("avg_purchase_per_user")
    )
    window_spec = Window.orderBy(col("user_count").desc())
    return state_aggs.withColumn("user_count_rank", rank().over(window_spec))

def write_data(df, output_path):
    df.write.option("partitionOverwriteMode", "dynamic") \
        .format("delta").mode("overwrite").partitionBy("date").parquet(output_path)


input_path = "s3://initial_users_bucket"
output_path = "s3://aggregated_users_bucket"
dbutils.widgets.text("geo", "US", "Geographical Region")
dbutils.widgets.text("date", datetime.now().strftime("%Y-%m-%d"), "Date")
geo = dbutils.widgets.get("geo")
date = dbutils.widgets.get("date")
df = read_data(spark, input_path)
filtered_df = filter_data(df, geo, date)
agg_df = aggregate_state_data(df_filtered)
write_data(agg_df, output_path)