from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.hooks.base import BaseHook
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
}

with DAG(
    'spark_jobs_dag',
    default_args=default_args,
    schedule_interval=None,  
) as dag:

    aws_connection = BaseHook.get_connection('aws_default')
    aws_access_key_id = aws_connection.login
    aws_secret_access_key = aws_connection.password
    aws_session_token = Variable.get("AWS_SESSION_TOKEN", "")

    spark_config = {
        "spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.508",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
        "spark.hadoop.fs.s3a.region": "us-east-1",
    }

    env_vars = {
        'AWS_ACCESS_KEY_ID': aws_access_key_id,
        'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
        'AWS_SESSION_TOKEN': aws_session_token,  
    }

    bronze_customers = SparkSubmitOperator(
        task_id='bronze_customers',
        application='bronze/customers.py',  
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    bronze_order_items = SparkSubmitOperator(
        task_id='bronze_order_items',
        application='bronze/order_items.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    bronze_orders = SparkSubmitOperator(
        task_id='bronze_orders',
        application='bronze/orders.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    silver_customers = SparkSubmitOperator(
        task_id='silver_customers',
        application='silver/customers.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    silver_order_items = SparkSubmitOperator(
        task_id='silver_order_items',
        application='silver/order_items.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    silver_orders = SparkSubmitOperator(
        task_id='silver_orders',
        application='silver/orders.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    gold = SparkSubmitOperator(
        task_id='gold',
        application='gold/summary.py',
        conf=spark_config,  
        env_vars=env_vars,
        dag=dag
    )

    bronze_tasks = [bronze_customers, bronze_orders, bronze_order_items]
    silver_tasks = [silver_customers, silver_orders, silver_order_items]

    for task in bronze_tasks:
        task >> silver_tasks  

    for task in silver_tasks:
        task >> gold
