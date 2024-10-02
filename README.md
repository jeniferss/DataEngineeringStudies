# Apache Airflow & Spark

This repository is intended for orchestrating Spark applications using the Apache Airflow tool

![alt text](images/image.png)

## Table of Contents

1. [Technologies](#technologies)
2. [Install and Run](#install-and-run)
3. [About](#about)
4. [Databricks Lakehouse Architecture](#databricks-lakehouse-architecture)

## Technologies

A list of technologies used within the project:

* [Python](https://www.python.org): Version 3.12
* [Pyspark](https://spark.apache.org/docs/latest/api/python/index.html): Version 3.5.3
* [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html): Version 2.10.2

## Install and Run

```bash
# Clone this repo
$ git clone git@github.com:jeniferss/DataEngineeringStudies.git
```

### Windows

```bash
# Create a virtual environment
$ python -m venv venv

# Activate your virtual environment
$ venv\Scripts\activate

# Install requirements
$ pip install -r requirements.txt

```

### MacOS & Linux

```bash
# Create a virtual environment
python3 -m venv venv # or virtualenv venv

# Activate your virtual environment
source venv/bin/activate

# Install requirements
$ pip install -r requirements.txt

```

### Config and Run Apache Airflow
*Ensure that Apache Airflow is installed on your machine.*

If this is the first time you are running Apache on your machine, you need to start the database and create a user to access the web client. To do this, you can:

```bash
# Start the database 
$ airflow db init

# Cretae admin user
$ airflow users create \
    --username admin \
    --firstname FirstName \
    --lastname LastName \
    --role Admin \
    --email yourmail@email.com \
    --password yourpass
```

To ensure that Airflow recognizes the DAG developed for this project, you can follow these steps. However, remember that this is only a temporary transformation, so don’t forget to change the DAG path back to the original version.

```bash
# Open the terminal and go to the root path
# Go to airflow folder
$ cd airflow

# Open airflow config file
$ gedit airflow.cfg

# Comment out the existing `dags_folder` setting and replace it with a new line specifying the path to the DAG folder for this repository.

# dags_folder = /home/youruser/airflow/dags
dags_folder = /home/your/path/to/this/repo/DataEngineeringStudies/dags
```

Finally, you can run Airflow

```bash
# Run webserver
$ airflow webserver --port 8080

# Run scheduler
$ airflow scheduler
```

### Apache Airflow Webserver

Webserver will start at: `http://127.0.0.1:8080`

From here, you can access the address above in your browser and log in. 

The first configuration of the web server should be to change the host in Airflow. To do this, go to Admin > Connections > Search for "spark_default" > Change the "Host" field from "yarn" to "local" and save.

Then, you can go to the "Search Dags" field and search for "spark_jobs_dag." Click on the search result, and you will have access to the interface related to the created Airflow instance. You can execute it by clicking the "Trigger DAG" button in the upper right corner of the screen, where you can observe the execution order and whether the Spark applications were successful or not. You can verify this by looking in the repository for each of the bronze, silver, and gold folders, where a subfolder called `parquet` will be created.


## About

The objective of this activity is to learn about orchestrating Spark applications using the Apache Airflow tool. Therefore, the requirements listed below have been met, and a bit about how it works and how to validate the results has been mentioned in the sections above.

### Part 01
- [x] Install and test Airflow with simple Python programs

### Part 02
- [x] Research Databricks Lakehouse architecture

### Part 03
- [x] Create the directory structure of a Lakehouse (landing, bronze, silver, gold)
- [x] Copy the JSON files for customers, orders, and order_items from the landing directory to the bronze directory
- [x] Bronze: perform transformation of JSON files to Parquet
- [x] Silver: rename the columns by removing the prefixes from each of them
- [x] Gold: create a dataset that shows the following columns: city, state, order quantity, and order value

### Part 04
- [x] Create an Airflow instance that executes all PySpark jobs, parallelizing the execution of the bronze and silver layers

## Databricks Lakehouse Architecture

The Medallion Architecture is a data design pattern used to logically organize data in a lakehouse, aimed at progressively enhancing the structure and quality of data as it flows through each layer of the architecture. The layers include Bronze (raw data), Silver (cleaned and transformed data), and Gold (data ready for analysis).
