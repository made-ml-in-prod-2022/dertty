import pandas as pd
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


def predict(model_path, raw_file_location, predictions_file_location):
    clf = load(model_path)
    X = pd.read_csv(raw_file_location + 'data.csv')
    pd.DataFrame(clf.predict(X)).to_csv(predictions_file_location + 'predictions.csv', index=False)


def data_prepocessing(raw_file_location, processed_file_location):
    X = pd.read_csv(raw_file_location + 'data.csv')
    y = pd.read_csv(raw_file_location + 'target.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    X_train.to_csv(processed_file_location + 'data_train.csv', index=False)
    X_test.to_csv(processed_file_location + 'data_test.csv', index=False)

    y_train.to_csv(processed_file_location + 'target_train.csv', index=False)
    y_test.to_csv(processed_file_location + 'target_test.csv', index=False)


def tune_model(processed_file_location, ti):
    X_train = pd.read_csv(processed_file_location + 'data_train.csv')
    y_train = pd.read_csv(processed_file_location + 'target_train.csv').iloc[:, 0].values

    clf = RandomForestClassifier(max_depth=5, n_estimators=50)
    max_depth = list(range(2, 10, 2))
    param_grid = dict(max_depth=max_depth)

    grid = GridSearchCV(clf, param_grid, cv=3, scoring='roc_auc', return_train_score=True)
    grid.fit(X_train, y_train)
    results = pd.DataFrame(grid.cv_results_)

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