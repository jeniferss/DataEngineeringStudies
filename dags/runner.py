from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
}

with DAG(
    'spark_jobs_dag', 
    default_args=default_args, 
    schedule_interval='@once'
) as dag:

    bronze_customers = SparkSubmitOperator(
        task_id='bronze_customers',
        application='bronze/customers.py',
        dag=dag,
    )

    bronze_order_items = SparkSubmitOperator(
        task_id='bronze_order_items',
        application='bronze/order_items.py',
        dag=dag,
    )

    bronze_orders = SparkSubmitOperator(
        task_id='bronze_orders',
        application='bronze/orders.py',
        dag=dag,
    )

    silver_customers = SparkSubmitOperator(
        task_id='silver_customers',
        application='silver/customers.py',
        dag=dag,
    )

    silver_order_items = SparkSubmitOperator(
        task_id='silver_order_items',
        application='silver/order_items.py',
        dag=dag,
    )

    silver_orders = SparkSubmitOperator(
        task_id='silver_orders',
        application='silver/orders.py',
        dag=dag,
    )

    gold = SparkSubmitOperator(
        task_id='gold',
        application='gold/summary.py',
        dag=dag,
    )
    
    bronze_tasks = [bronze_customers, bronze_order_items, bronze_orders]
    silver_tasks = [silver_customers, silver_order_items, silver_orders]

    for task in bronze_tasks:
        task >> silver_tasks  

    for task in silver_tasks:
        task >> gold
