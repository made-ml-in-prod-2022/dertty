# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../config", config_name="config")
def main(cfg: DictConfig):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df = pd.read_csv(Path(hydra.utils.get_original_cwd(), cfg.filename))
    logger.info(f'file {Path(hydra.utils.get_original_cwd(), cfg.filename)} have been read')
    path_base_part = f'{cfg.processed_folder}/{Path(cfg.filename).stem}'
    features = cfg.cat_cols + cfg.num_cols + [cfg.target_col, ]
    df[features].to_csv(Path(hydra.utils.get_original_cwd(), f'{path_base_part}.csv'), index=False)
    logger.info(f'file have been saved to {Path(hydra.utils.get_original_cwd(), f"{path_base_part}.csv")}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
