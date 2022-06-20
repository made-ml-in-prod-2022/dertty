from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.log.logging_mixin import LoggingMixin

from datetime import datetime, timedelta
import logging

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification


logger = logging.getLogger("airflow.task")


def generate_xy(raw_file_location):
    X, y = make_classification(n_features=2, n_redundant=0, n_informative=2, random_state=1, n_clusters_per_class=1)
    rng = np.random.RandomState(2)
    X += 2 * rng.uniform(size=X.shape)

    pd.DataFrame(X).to_csv(raw_file_location + 'data.csv', index=False)
    pd.DataFrame(y).to_csv(raw_file_location + 'target.csv', index=False)
    LoggingMixin().log.info(f"Samples are stored in {file_location}")


with DAG(
        'data_preparation',
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

    raw_mkdir = BashOperator(
        task_id='raw_mkdir',
        bash_command='mkdir -p /opt/airflow/data/raw/{{ ds }}',
        dag=dag,
    )

    generate_xy_task = PythonOperator(
        task_id='build_project',
        python_callable=generate_xy,
        dag=dag,
        op_kwargs={'raw_file_location': '/opt/airflow/data/raw/{{ ds }}/'},
    )

    raw_mkdir >> generate_xy_task
