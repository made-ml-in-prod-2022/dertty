from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import Variable

from datetime import datetime, timedelta
import logging

import numpy as np
import pandas as pd
from joblib import dump, load

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

logger = logging.getLogger("airflow.task")


def data_prepocessing(raw_file_location, processed_file_location):
    X = pd.read_csv(raw_file_location + 'data.csv')
    y = pd.read_csv(raw_file_location + 'target.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    X_train.to_csv(processed_file_location + 'data_train.csv', index=False)
    LoggingMixin().log.info(f"X_train are stored in {processed_file_location}data_train.csv")
    X_test.to_csv(processed_file_location + 'data_test.csv', index=False)
    LoggingMixin().log.info(f"X_test are stored in {processed_file_location}data_test.csv")

    y_train.to_csv(processed_file_location + 'target_train.csv', index=False)
    LoggingMixin().log.info(f"y_train are stored in {processed_file_location}target_train.csv")
    y_test.to_csv(processed_file_location + 'target_test.csv', index=False)
    LoggingMixin().log.info(f"y_test are stored in {processed_file_location}target_test.csv")


def tune_model(processed_file_location, ti):
    X_train = pd.read_csv(processed_file_location + 'data_train.csv')
    y_train = pd.read_csv(processed_file_location + 'target_train.csv').iloc[:, 0].values

    clf = RandomForestClassifier(max_depth=5, n_estimators=50)
    max_depth = list(range(2, 10, 2))
    param_grid = dict(max_depth=max_depth)

    grid = GridSearchCV(clf, param_grid, cv=3, scoring='roc_auc', return_train_score=True)
    grid.fit(X_train, y_train)
    results = pd.DataFrame(grid.cv_results_)

    LoggingMixin().log.info(f"mean_train_score {results.mean_train_score.mean()}")
    LoggingMixin().log.info(f"mean_test_score {results.mean_test_score.mean()}")

    LoggingMixin().log.info(f"best_params {grid.best_params_}")

    ti.xcom_push(key='max_depth', value=grid.best_params_['max_depth'])


def fit_model(processed_file_location, model_file_location, ti):
    X_train = pd.read_csv(processed_file_location + 'data_train.csv')
    y_train = pd.read_csv(processed_file_location + 'target_train.csv').iloc[:, 0].values
    clf = RandomForestClassifier(max_depth=ti.xcom_pull(key="max_depth"), n_estimators=50)
    clf.fit(X_train, y_train)
    dump(clf, model_file_location + 'model.joblib')


def evaluate_model(processed_file_location, model_file_location, ti):
    clf = load(model_file_location + 'model.joblib')
    X_test = pd.read_csv(processed_file_location + 'data_test.csv')
    y_test = pd.read_csv(processed_file_location + 'target_test.csv').iloc[:, 0].values

    score = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
    ti.xcom_push(key='model_perfomance', value=score)


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
