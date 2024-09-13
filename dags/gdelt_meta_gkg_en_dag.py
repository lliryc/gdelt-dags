from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from tasks.download_compressed_csv import write_raw_gkg_content_to_db

def gdelt_upload_meta_gkg_en_15min_task(**kwargs):
    execution_date:datetime = kwargs['execution_date']
    date_str = execution_date.strftime("%Y%m%d%H%M%S")
    url = f"http://data.gdeltproject.org/gdeltv2/{date_str}.gkg.csv.zip"
    write_raw_gkg_content_to_db(url)
    return True

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gdelt_upload_meta_gkg_en_15min_backfill',
    default_args=default_args,
    description='A DAG that prints its run date',
    schedule_interval=timedelta(minutes=15),
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 9, 12),
    catchup=True,
    max_active_runs=25
)

task_upload = PythonOperator(
    task_id='gdelt_upload_meta_gkg_en_15min_task',
    python_callable=gdelt_upload_meta_gkg_en_15min_task,
    provide_context=True,
    dag=dag,
)

task_upload