from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, 
    StructField, 
    StringType, 
    IntegerType, 
    ArrayType, 
    FloatType
)


class OrderConsumer:
    def __init__(
            self, 
            appname: str = "OrderConsumer",
            bootstrap_server: str = "localhost:9092",
            topic: str = "orders"
        ) -> None:

        self.appname = appname
        self.bootstrap_server = bootstrap_server
        self.topic = topic

        self.spark = SparkSession \
            .builder \
            .appName(self.appname) \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()

        self.order_schema = StructType([
            StructField("id", StringType(), False),
            StructField("date", StringType(), False),
            StructField("client", StructType([
                StructField("name", StringType(), False),
                StructField("document", StringType(), False)
            ]), False),
            StructField("items", ArrayType(StructType([
                StructField("name", StringType(), False),
                StructField("quantity", IntegerType(), False),
                StructField("price", FloatType(), False)
            ])), False),
            StructField("total", FloatType(), False)
        ])

    def main(self) -> None:
        orders = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_server) \
            .option("subscribe", self.topic) \
            .load()

        orders = orders.selectExpr("CAST(value AS STRING) AS orders")
        orders = orders.selectExpr("orders", f"from_json(orders, '{self.order_schema.simpleString()}') AS order_data")

        formatted_orders = orders.select(
            F.explode("order_data.items").alias("item"), 
            "order_data.id", 
            "order_data.date", 
            "order_data.client", 
            "order_data.total"
        )

        aggregated_orders = formatted_orders \
            .groupBy("item.name") \
            .agg(
                F.sum("item.quantity").alias("quantity"),
                F.round(
                    F.sum(F.col("item.quantity") * F.col("item.price")), 
                    2
                ).alias("revenue")
            ) \
            .orderBy(F.col("revenue").desc())

        query = aggregated_orders.writeStream \
            .outputMode("complete") \
            .format("console") \
            .start()

        query.awaitTermination()


try:
    print("\033[92m" + "\n-----------------  INCIANDO CONSUMIDOR -----------------\n" + "\033[0m")
    order_consumer = OrderConsumer()
    order_consumer.main()
except KeyboardInterrupt:
    print("\033[93m" + "\n-----------------  FINALIZANDO CONSUMIDOR -----------------\n" + "\033[0m")
except Exception as error:
    print("\033[91m" + f"\n----------------- ERRO -----------------\n{error}\n" + "\033[0m")
