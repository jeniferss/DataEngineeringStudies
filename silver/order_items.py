import os

from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('Rename Order Items').getOrCreate()

    filepath = os.path.join('bronze', 'parquets', 'order_item.parquet')
    dataset = spark.read.parquet(filepath)

    prefix = 'order_item_'
    columns = [column.replace(prefix, '') for column in dataset.columns]

    renamed = dataset.toDF(*columns)
    renamed.show(5)
    
    outputdir =  os.path.join('silver', 'parquets', 'order_item.parquet')
    renamed.write.parquet(outputdir, mode="overwrite")

    spark.stop()
