# ML in prod MADE:  homework3

### Запуск сервера
Стартуют вебсервер, бд, воркер и т.д. Образ содержит mlflow и poetry.
```console
cd airflow_ml_dags
docker compose up --force-recreate --build -d
```
