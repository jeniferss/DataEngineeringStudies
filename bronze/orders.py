from pyspark.sql import SparkSession


if __name__ == '__main__':
    spark = SparkSession.builder.appName('Import Orders').getOrCreate()

    BUCKET_NAME = 'js-s3files'

    input_path = "sparkairflow/landing/orders.json"
    print(f"Importando dados do arquivo {input_path}")
    dataset = spark.read.json(f"s3a://{BUCKET_NAME}/{input_path}")
    dataset.show(5)

    output_path = 'sparkairflow/bronze/orders.parquet'
    print(f"Salvando dados no arquivo {output_path}")
    dataset.write.parquet(f"s3a://{BUCKET_NAME}/{output_path}", mode="overwrite")
    
    spark.stop()
