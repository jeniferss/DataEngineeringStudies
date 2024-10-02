import os

from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('Rename Customers').getOrCreate()

    filepath = os.path.join('bronze', 'parquets', 'customers.parquet')
    dataset = spark.read.parquet(filepath)

    prefix = 'customer_'
    columns = [column.replace(prefix, '') for column in dataset.columns]

    renamed = dataset.toDF(*columns)
    renamed.show(5)
    
    outputdir =  os.path.join('silver', 'parquets', 'customers.parquet')
    renamed.write.parquet(outputdir, mode="overwrite")

    spark.stop()
