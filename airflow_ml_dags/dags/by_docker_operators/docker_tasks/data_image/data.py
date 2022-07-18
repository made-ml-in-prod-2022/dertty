import numpy as np
import pandas as pd

from sklearn.datasets import make_classification

import click


@click.command()
@click.option('--raw_file_location')
def generate_xy(raw_file_location):
    X, y = make_classification(n_features=2, n_redundant=0, n_informative=2, random_state=1, n_clusters_per_class=1)
    rng = np.random.RandomState(2)
    X += 2 * rng.uniform(size=X.shape)

    pd.DataFrame(X).to_csv(raw_file_location + 'data.csv', index=False)
    pd.DataFrame(y).to_csv(raw_file_location + 'target.csv', index=False)


if __name__ == '__main__':
    generate_xy()
