import os

from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('Import Order Item').getOrCreate()

    filepath = os.path.join('landing', 'order_item.json')
    dataset = spark.read.json(filepath)

    dataset.show(5)
    
    outputdir =  os.path.join('bronze', 'parquets', 'order_item.parquet')
    dataset.write.parquet(outputdir, mode="overwrite")

    spark.stop()
