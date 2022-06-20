from airflow.models import Variable
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.log.logging_mixin import LoggingMixin

from datetime import datetime, timedelta
import logging

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


logger = logging.getLogger("airflow.task")


def predict(predictions_file_location):
    model_path = Variable.get("model_path")
    clf = load(model_path)
    X = pd.read_csv(raw_file_location + 'data.csv')
    clf.predict(X).to_csv(predictions_file_location + 'predictions.csv', index=False)


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

    predictions_mkdir = BashOperator(
        task_id='predictions_mkdir',
        bash_command='mkdir -p /opt/airflow/data/predictions/{{ ds }}',
        dag=dag,
    )

    predict_task = PythonOperator(
        task_id='predict',
        python_callable=predict,
        dag=dag,
        op_kwargs={'predictions_file_location': '/opt/airflow/data/predictions/{{ ds }}/'},
    )

    predictions_mkdir >> predict_task
