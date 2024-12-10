import os
import shutil

from pyspark.sql import *

if __name__ == '__main__':
    warehouse_path = os.path.join('spark-warehouse')
    if os.path.exists(warehouse_path):
        shutil.rmtree(warehouse_path)
    
    spark = SparkSession.builder.appName('Rename Customers').getOrCreate()

    BUCKET_NAME = 'js-s3files'

    orders_filepath = 'sparkairflow/silver/orders.parquet'
    customers_filepath = 'sparkairflow/silver/customers.parquet'
    order_items_filepath = 'sparkairflow/silver/order_item.parquet'
    
    Orders = spark.read.parquet(f"s3a://{BUCKET_NAME}/{orders_filepath}")
    Customers = spark.read.parquet(f"s3a://{BUCKET_NAME}/{customers_filepath}")
    OrderItems = spark.read.parquet(f"s3a://{BUCKET_NAME}/{order_items_filepath}")

    spark.sql("CREATE DATABASE IF NOT EXISTS Sales")
    spark.sql("show databases").show()

    spark.sql("USE Sales")

    Orders.write.saveAsTable("Orders")
    Customers.write.saveAsTable("Customers")
    OrderItems.write.saveAsTable("OrderItems")

    spark.sql("show tables").show()

    Summary = spark.sql("""
        SELECT 
            CUSTOMER.city,
            CUSTOMER.state,
            COUNT(DISTINCT ORDER.id) AS order_quantity,
            SUM(ITEMS.subtotal) AS total_value
        FROM orderitems AS ITEMS
        INNER JOIN orders AS ORDER ON ITEMS.order_id = ORDER.id
        INNER JOIN customers AS CUSTOMER ON ORDER.customer_id = CUSTOMER.id
        GROUP BY CUSTOMER.city, CUSTOMER.state
        ORDER BY CUSTOMER.state, CUSTOMER.city;
    """)

    Summary.show()
     
    output_path = 'sparkairflow/gold/summary.parquet'
    print(f"Salvando dados no arquivo {output_path}")
    Summary.write.parquet(f"s3a://{BUCKET_NAME}/{output_path}", mode="overwrite")

    spark.stop()
