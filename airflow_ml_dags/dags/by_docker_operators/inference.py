from airflow.models import Variable
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow.utils.log.logging_mixin import LoggingMixin

from datetime import datetime, timedelta
import logging


logger = logging.getLogger("airflow.task")


with DAG(
        'inference',
        schedule_interval='@daily',
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

    predict_task = DockerOperator(
        image="model_image",
        command="--raw_file_location=/data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="docker-generate-xy",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/aleksandr/Documents/projects/made-ml-in-prod-2022/dertty/airflow_ml_dags/data", target="/data", type='bind')]
    )

    predict_task
