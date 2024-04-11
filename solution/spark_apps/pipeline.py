from pyspark.sql import SparkSession, functions
from os import path
from schemas import customers_schema, orders_schema, deliveries_schema

spark = SparkSession.builder.appName("PipelineExercise").config("spark.driver.extraClassPath", path.join(path.dirname(path.dirname(path.abspath(__file__))), "jars", "postgresql-42.7.3.jar")).getOrCreate()
spark.sparkContext.setLogLevel("OFF")
spark.conf.set("spark.sql.streaming.stateStore.providerClass","org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")

#set data and archive directories
data_dir = path.join(path.dirname(path.dirname(path.abspath(__file__))), "data")
data_archive = path.join(path.dirname(path.dirname(path.abspath(__file__))), "archive")

#stream data into dataframes
customers_df = spark.readStream \
    .schema(customers_schema) \
    .option("multiline", "true") \
    .option("cleanSource", "archive") \
    .option("sourceArchiveDir", data_archive) \
    .option("spark.sql.streaming.fileSource.cleaner.numThreads", "10") \
    .json(path.join(data_dir, "Customers"))
# customers_df = customers_df.withColumnRenamed("Number of employees", "Number of Employees")
customers_df = customers_df.select(*[functions.col(col_name).alias(col_name.replace(" ", "_")) for col_name in customers_df.columns])


deliveries_df = spark.readStream \
    .schema(deliveries_schema) \
    .option("header", "true") \
    .option("cleanSource", "archive") \
    .option("sourceArchiveDir", data_archive) \
    .option("spark.sql.streaming.fileSource.cleaner.numThreads", "10") \
    .csv(path.join(data_dir, "Deliveries"))
deliveries_df = deliveries_df.withColumn("Order_ID", functions.regexp_extract(deliveries_df["Order_ID"], r"YR-(\d+),0", 1))
deliveries_df = deliveries_df.select(*[functions.col(col_name).alias(col_name.replace(" ", "_")) for col_name in deliveries_df.columns])


orders_df = spark.readStream \
    .schema(orders_schema) \
    .option("header", "true") \
    .option("cleanSource", "archive") \
    .option("sourceArchiveDir", data_archive).csv(path.join(data_dir, "Orders"))
orders_df = orders_df.select(*[functions.col(col_name).alias(col_name.replace(" ", "_")) for col_name in orders_df.columns])
# orders_df = orders_df.drop("Discount").drop("Tip")
orders_df = orders_df.withColumnRenamed("Discount", "Order_Discount").withColumnRenamed("Tip", "Order_Tip")

#join dataframes
combined_df = orders_df.join(deliveries_df, "Order_ID", "inner").join(customers_df, "Customer_ID", "inner")

#apply aggregation metrics and write datastream to postgres database
combined_df.withWatermark('Order_Time', '10 minutes').groupBy(functions.window('Order_Time', "10 days"),"Customer_ID").agg(
    functions.sum("Order_Total").alias("Total_Order_Amount"), 
    functions.avg("Order_Total").alias("Average_Order_Amount"),
    functions.count("Order_ID").alias("Order_Count"),
    functions.max("Order_Total").alias("Highest_Order_Amount"),
    functions.min("Order_Total").alias("Lowest_Order_Amount"),
    functions.sum("Quantity").alias("Total_Quantity_Ordered"),
    functions.avg("Quantity").alias("Average_Quantity_Per_Ordered"),
    functions.sum("Distance(m)").alias("Total_Delivery_Distance"),
    functions.avg("Distance(m)").alias("Average_Delivery_Distance"),
    functions.count("SKU").alias("Distict_Products")
    ).withColumn("start_timestamp",functions.col("window.start")).withColumn("end_timestamp", functions.col("window.end")).drop("window") \
     .writeStream \
     .foreachBatch(lambda batch_df, batch_id: batch_df.write 
     .format("jdbc") \
     .option("url", "jdbc:postgresql://db/ecommerce") \
     .option("dbtable", "public.analytics") \
     .option("user", "postgres") \
     .option("password", "postgres") \
     .save(mode="append")) \
     .outputMode("append").start().awaitTermination()
#    .writeStream.format("console").option('truncate', 'false').outputMode("append").start().awaitTermination()



