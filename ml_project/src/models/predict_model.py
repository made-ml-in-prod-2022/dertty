# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import hydra
from omegaconf import DictConfig
from joblib import load


@hydra.main(config_path="../config", config_name="config.yaml")
def main(cfg: DictConfig):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    pipe = load(Path(hydra.utils.get_original_cwd(), cfg.model_path_to_save, cfg.model.name))
    df = pd.read_csv(Path(hydra.utils.get_original_cwd(), cfg.processed_folder, Path(cfg.filename).name))
    X = df[cfg.cat_cols + cfg.num_cols]
    X['predict'] = pipe.predict_proba(X)[:, 1]
    
    if Path(cfg.result_folder).name[-3:] == 'csv':
        X.to_csv(Path(hydra.utils.get_original_cwd(), cfg.result_folder), index=False)
        logger.info(
            f'mdoel file have been saved to {Path(hydra.utils.get_original_cwd(), cfg.result_folder)}')
    else:
        X.to_csv(Path(hydra.utils.get_original_cwd(), cfg.result_folder, Path(cfg.filename).name), index=False)
        logger.info(
            f'model file have been saved to {Path(hydra.utils.get_original_cwd(), cfg.result_folder, Path(cfg.filename).name)}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
