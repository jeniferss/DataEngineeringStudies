import os
import shutil

from pyspark.sql import *

if __name__ == '__main__':
    warehouse_path = os.path.join('spark-warehouse')
    if os.path.exists(warehouse_path):
        shutil.rmtree(warehouse_path)
    
    spark = SparkSession.builder.appName('Rename Customers').getOrCreate()

    orders_filepath = os.path.join('silver', 'parquets', 'orders.parquet')
    customers_filepath = os.path.join('silver', 'parquets', 'customers.parquet')
    order_items_filepath = os.path.join('silver', 'parquets', 'order_item.parquet')
    
    Orders = spark.read.parquet(orders_filepath)
    Customers = spark.read.parquet(customers_filepath)
    OrderItems = spark.read.parquet(order_items_filepath)

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
     
    outputdir =  os.path.join('gold', 'parquets', 'summary.parquet')
    Summary.write.parquet(outputdir, mode="overwrite")

    spark.stop()
