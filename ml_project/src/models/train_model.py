# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import hydra
from omegaconf import DictConfig
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegressionCV
from joblib import dump
from transformers import *
from sklearn.ensemble import RandomForestClassifier


@hydra.main(config_path="../config", config_name="config.yaml")
def main(cfg: DictConfig):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    union = FeatureUnion([("ohe", MultiOneHotEncoder(cat_columns=cfg.cat_cols)),
                          ("numeric", FeatureSelector(num_columns=cfg.num_cols))])

    if cfg.model.name == 'logreg':
        model = LogisticRegressionCV(cv=cfg.model.cv, max_iter=cfg.model.max_iter, random_state=cfg.random_state)
    else:
        model = RandomForestClassifier(max_depth=cfg.model.max_depth, random_state=cfg.random_state)
    pipe = Pipeline(
        steps=[
            ('preproc', union),
            ('model', model)])

    df = pd.read_csv(Path(hydra.utils.get_original_cwd(), cfg.filename))
    X = df[cfg.cat_cols + cfg.num_cols]
    y = df[cfg.target_col]
    pipe.fit(X, y)
    dump(pipe, Path(hydra.utils.get_original_cwd(), cfg.model_path_to_save, cfg.model.name))
    logger.info(f'mdoel file have been saved to {Path(hydra.utils.get_original_cwd(), cfg.model_path_to_save, cfg.model.name)}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
