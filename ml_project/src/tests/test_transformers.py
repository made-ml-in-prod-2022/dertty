import pytest
from faker import Faker
import pandas as pd
from ml_project.src.models.transformers import MultiOneHotEncoder, FeatureSelector

fake = Faker()


def test_one_hot_encoder():
    crypto_codes = []
    cur_codes = []
    for _ in range(5):
        crypto_codes.append(fake.cryptocurrency_code())
    for _ in range(5):
        cur_codes.append(fake.currency_code())
    df = pd.DataFrame({'crypto': crypto_codes, 'cur': cur_codes})
    ohes = MultiOneHotEncoder(cat_columns=['crypto', 'cur'])
    ohes.fit(df)
    res = ohes.transform(df)
    assert res.shape[0] == 5, 'Лишние строки'
    assert res.shape[1] == len(set(cur_codes + crypto_codes)), 'Колонок меньше, чем уникальных значений'

    ohes = MultiOneHotEncoder(cat_columns=['crypto'])
    ohes.fit(df)
    res = ohes.transform(df)
    assert res.shape[1] == len(set(crypto_codes)), 'Неправильная обработка колонок'