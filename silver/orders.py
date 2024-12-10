import os

from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('Rename Orders').getOrCreate()

    BUCKET_NAME = 'js-s3files'

    input_path = "sparkairflow/bronze/orders.parquet"
    print(f"Importando dados do arquivo {input_path}")
    dataset = spark.read.parquet(f"s3a://{BUCKET_NAME}/{input_path}")

    prefix = 'order_'
    columns = [column.replace(prefix, '') for column in dataset.columns]

    renamed = dataset.toDF(*columns)
    renamed.show(5)
    
    output_path = 'sparkairflow/silver/orders.parquet'
    print(f"Salvando dados no arquivo {output_path}")
    renamed.write.parquet(f"s3a://{BUCKET_NAME}/{output_path}", mode="overwrite")

    spark.stop()
