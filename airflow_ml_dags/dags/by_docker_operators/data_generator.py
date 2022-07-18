from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

from datetime import datetime, timedelta
import logging


logger = logging.getLogger("airflow.task")


with DAG(
        'docker_data_preparation',
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

    generate_xy_task = DockerOperator(
        image="data_image",
        command="--raw_file_location=data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="docker-generate-xy",
        auto_remove=True,
        do_xcom_push=True,
        mount_tmp_dir=False,
        docker_url='unix:///var/run/docker.sock',
        api_version='auto',
        # mounts=[Mount(source="/Users/aleksandr/Documents/projects/made-ml-in-prod-2022/dertty/airflow_ml_dags/data", target="data", type='bind')]
    )

    generate_xy_task
