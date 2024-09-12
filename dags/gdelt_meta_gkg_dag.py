from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def print_dag_run_date(**kwargs):
    execution_date = kwargs['execution_date']
    print(f'DAG Run Date: {execution_date}')
    return f'DAG Run Date: {execution_date}'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'print_dag_run_date',
    default_args=default_args,
    description='A DAG that prints its run date',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

task_print_date = PythonOperator(
    task_id='print_dag_run_date',
    python_callable=print_dag_run_date,
    provide_context=True,
    dag=dag,
)

task_print_date