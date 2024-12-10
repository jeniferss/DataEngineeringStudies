import io

from pyspark.sql import SparkSession
from settings import *


if __name__ == '__main__':
    spark = SparkSession.builder \
    .appName('Import Customers') \
    .config(
        "spark.jars.packages", 
        "org.apache.hadoop:hadoop-aws:3.3.1,"
        "com.amazonaws:aws-java-sdk:1.12.185"
    ) \
    .getOrCreate()

    spark.conf.set("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    spark.conf.set("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    spark.conf.set("spark.hadoop.fs.s3a.session.token", AWS_SESSION_TOKEN)
    spark.conf.set("spark.hadoop.fs.s3a.region", AWS_REGION)  

    input_path = "sparkairflow/landing/customers.json"
    print(f"Importando dados do arquivo {input_path}")
    dataset = spark.read.json(f"s3a://{BUCKET_NAME}/{input_path}")
    dataset.show(5)

    output_path = 'sparkairflow/bronze/customers.parquet'
    print(f"Salvando dados no arquivo {output_path}")
    dataset.write.parquet(f"s3a://{BUCKET_NAME}/{output_path}", mode="overwrite")
    
    spark.stop()
