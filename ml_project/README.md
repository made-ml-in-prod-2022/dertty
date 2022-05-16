ml_project
==============================

MADE ML in prod homework #1

# ML production ready project example
## How to use
#### Dag of train pipeline is implemented with *Makefile*.
To run whole train pipeline including requirements installation and preprocessing on default dataset use:
```commandline
make train
```
To run predict pipeline including requirements installation and preprocessing on default dataset use:
```commandline
make predict model=logreg filename=data/raw/heart_cleveland_upload.csv result_folder=data/results/heart_cleveland_upload.csv
```
To run train pipeline use another configs use:
```commandline
make train CONFIG=logreg
```
To create EDA report in report folder:
``commandline
make eda
```

## Project about
- **Data source**:\
  Kaggle dataset [Heart Disease Cleveland UCI](https://www.kaggle.com/datasets/cherngs/heart-disease-cleveland-uci) is used in the project
- **Project organization**:\
The schema of project organization is represented in *docs/README_project_organization.md*
Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    │
    ├── models             <- Trained and serialized models
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    │
    ├── configs            <- Pipeline configs.
    │   ├── configs.yaml 
    │   └── model        <- Model configs
    │       ├── logreg.yaml
    │       └── tree.yaml
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │       │                 predictions
    │       ├── transformers.py
    │       ├── predict_model.py
    │       └── train_model.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
