from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
import copy
from scipy.sparse import hstack
from sklearn.exceptions import NotFittedError


class MultiOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cat_columns):
        self.cat_columns = cat_columns
        self.ohes = {}
        self.is_fitted_flg: bool = False

    def is_fitted(self) -> None:
        if not self.is_fitted_flg:
            raise NotFittedError('MultiOneHotEncoder is not fitted')

    def fit(self, X, y=None):
        for column in self.cat_columns:
            ohe = OneHotEncoder(handle_unknown='ignore')
            ohe.fit(X[[column]])
            self.ohes[column] = copy.deepcopy(ohe)
        self.is_fitted_flg = True
        return self

    def transform(self, X, y=None):
        self.is_fitted()
        data = []
        for column in self.ohes.keys():
            data.append(self.ohes[column].transform(X[[column]]))

        return hstack(data).todense()


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, num_columns):
        self.num_columns = num_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # no fit required
        return X[self.num_columns].fillna(0)