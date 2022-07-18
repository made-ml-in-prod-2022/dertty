# ML in prod MADE:  homework2

### Запуск сервера
```console
cd online_inference
uvicorn app:app --reload
```
### Команда предикт
```console
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'
```

### Команда для теста
```console
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 0,
  "sex": 0,
  "cp": 0,
  "trestbps": 0,
  "chol": 0,
  "fbs": 0,
  "restecg": 0,
  "thalach": 0,
  "exang": 0,
  "oldpeak": 0,
  "slope": 0,
  "ca": 0,
  "thal": 0
}'
```