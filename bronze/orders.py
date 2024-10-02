import os

from pyspark.sql import SparkSession


if __name__ == '__main__':
    spark = SparkSession.builder.appName('Import Orders').getOrCreate()

    filepath = os.path.join('landing', 'orders.json')
    dataset = spark.read.json(filepath)

    dataset.show(5)
    
    outputdir =  os.path.join('bronze', 'parquets', 'orders.parquet')
    dataset.write.parquet(outputdir, mode="overwrite")

    spark.stop()
