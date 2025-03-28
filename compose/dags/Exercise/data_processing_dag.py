from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
import os

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 1),
    'email': ['sergendel@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': 1, #timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'iris_etl_dag',
    default_args=default_args,
    description='ETL DAG for Iris dataset',
    schedule_interval='@daily',
    catchup=False,
)

# Task 1: Extract data
def extract_data(**kwargs):

    # data file path setting-----------------------------
    #df = pd.read_csv('dags/Exercise/data/Iris.csv')    # for airflow run
    #df = pd.read_csv('data/Iris.csv')                   # for local run

    # Dynamic data path --------------------------------------------------------
    # Solution is to use relative paths dynamically based on DAG file location:

    # Get the current file path (this script)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the path dynamically relative to this file
    csv_path = os.path.join(current_dir, 'data', 'Iris.csv')


    # Load your data
    df = pd.read_csv(csv_path)

    return df.to_json(orient='split')

# Task 2: Transform data
def transform_data(ti):
    species_mapping = {
        'Iris-setosa': 1,
        'Iris-versicolor': 2,
        'Iris-virginica': 3
    }
    iris_json = ti.xcom_pull(task_ids='extract_data_task')
    df = pd.read_json(iris_json, orient='split')

    df['SepalArea'] = df['SepalLengthCm'] * df['SepalWidthCm']
    df['PetalArea'] = df['PetalLengthCm'] * df['PetalWidthCm']
    df['Species'] = df['Species'].map(species_mapping)

    return df.to_json(orient='split')

# Task 3: Load data
def load_data(ti, execution_date):
    iris_json = ti.xcom_pull(task_ids='transform_data_task')
    df = pd.read_json(iris_json, orient='split')

    output_folder = 'dags/Exercise/data/transformed/'
    os.makedirs(output_folder, exist_ok=True)
    filename = f'iris_transformed_{execution_date.strftime("%Y-%m-%d")}.csv'
    df.to_csv(os.path.join(output_folder, filename), index=False)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data_task',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

# Task dependencies
extract_task >> transform_task >> load_task


if __name__ == "__main__":
    extract_data()