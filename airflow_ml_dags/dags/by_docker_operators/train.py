from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

from datetime import datetime, timedelta
import logging


logger = logging.getLogger("airflow.task")


with DAG(
        'get_model',
        schedule_interval='@weekly',
        catchup=False,
        max_active_runs=1,
        default_args={
            'owner': 'airflow',
            'depends_on_past': False,
            'start_date': datetime(2022, 6, 20),
            'retries': 0,
            'retry_delay': timedelta(seconds=15)
        }
) as dag:
    processed_mkdir = BashOperator(
        task_id='processed_mkdir',
        bash_command='mkdir -p /opt/airflow/data/processed/{{ ds }}',
        dag=dag,
    )

    models_mkdir = BashOperator(
        task_id='models_mkdir',
        bash_command='mkdir -p /opt/airflow/data/models/{{ ds }}',
        dag=dag,
    )

    data_prepocessing_task = PythonOperator(
        task_id='data_prepocessing',
        python_callable=data_prepocessing,
        dag=dag,
        op_kwargs={
            'raw_file_location': '/opt/airflow/data/raw/{{ ds }}/',
            'processed_file_location': '/opt/airflow/data/processed/{{ ds }}/'
        },
    )

    tune_model_task = PythonOperator(
        task_id='tune_model',
        python_callable=tune_model,
        dag=dag,
        op_kwargs={
            'processed_file_location': '/opt/airflow/data/processed/{{ ds }}/'
        },
    )

    fit_model_task = PythonOperator(
        task_id='fit_model',
        python_callable=fit_model,
        dag=dag,
        op_kwargs={
            'processed_file_location': '/opt/airflow/data/processed/{{ ds }}/',
            'model_file_location': '/opt/airflow/data/models/{{ ds }}/',
        },
    )

    evaluate_model_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        dag=dag,
        op_kwargs={
            'processed_file_location': '/opt/airflow/data/processed/{{ ds }}/',
            'model_file_location': '/opt/airflow/data/models/{{ ds }}/',
        },
    )

    processed_mkdir >> models_mkdir >> data_prepocessing_task >> tune_model_task >> fit_model_task >> evaluate_model_task
