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

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement

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
            .config(
                "spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,"
                "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0"
            ) \
            .config("spark.cassandra.connection.host", "127.0.0.1") \
            .config("spark.cassandra.auth.username", "cassandra") \
            .config("spark.cassandra.auth.password", "cassandra") \
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
    
    def setup_database(self):
        cassandra_host = "127.0.0.1"
        cassandra_port = 9042
        cassandra_user = "cassandra"  
        cassandra_password = "cassandra"  

        auth_provider = PlainTextAuthProvider(cassandra_user, cassandra_password)
        cluster = Cluster([cassandra_host], port=cassandra_port, auth_provider=auth_provider)
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS sales WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)

        session.set_keyspace("sales")

        session.execute("""
            CREATE TYPE IF NOT EXISTS client (
                document TEXT,
                name TEXT
            );
        """)

        session.execute("""
            CREATE TYPE IF NOT EXISTS item (
                name TEXT,
                price FLOAT,
                quantity INT
            );
        """)

        session.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id UUID PRIMARY KEY,
                date TEXT,
                client FROZEN<client>,
                items LIST<FROZEN<item>>,
                total float
            )
        """)

        session.shutdown()

    def main(self) -> None:
        self.setup_database()

        orders = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_server) \
            .option("subscribe", self.topic) \
            .load()

        orders = orders.selectExpr("CAST(value AS STRING) AS orders")
        orders = orders.select(F.from_json("orders", self.order_schema).alias("order_data"))

        if not orders:
            return

        orders = orders.select(
            F.col("order_data.id").alias("id"),
            F.col("order_data.date").alias("date"),
            F.col("order_data.client").alias("client"),
            F.col("order_data.items").alias("items"),
            F.col("order_data.total").alias("total")
        )

        def write_to_cassandra(batch_df, batch_id):
            print(f'Salvando batch {batch_id}')

            batch_df.write \
                .format("org.apache.spark.sql.cassandra") \
                .option("keyspace", "sales") \
                .option("table", "orders") \
                .mode("append") \
                .save()
        
        # Start the streaming query and write the output to Cassandra
        query = orders.writeStream \
            .foreachBatch(write_to_cassandra) \
            .outputMode("append") \
            .start()

        # Await termination
        query.awaitTermination()

try:
    print("\033[92m" + "\n-----------------  INCIANDO CONSUMIDOR -----------------\n" + "\033[0m")
    order_consumer = OrderConsumer()
    order_consumer.main()
except KeyboardInterrupt:
    print("\033[93m" + "\n-----------------  FINALIZANDO CONSUMIDOR -----------------\n" + "\033[0m")
except Exception as error:
    print("\033[91m" + f"\n----------------- ERRO -----------------\n{error}\n" + "\033[0m")
