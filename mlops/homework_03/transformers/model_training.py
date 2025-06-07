if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer

@transformer
def train_model(df, *args, **kwargs):
    dicts = df[['PULocationID', 'DOLocationID']].to_dict(orient='records')

    dv = DictVectorizer()
    X_train = dv.fit_transform(dicts)
    y_train = df['duration'].values

    model = LinearRegression()
    model.fit(X_train, y_train)

    print("Model intercept:", model.intercept_)

    return model, dv

@test
def test_output(output, *args) -> None:
    model, dv = output
    assert model is not None
    assert dv is not None
