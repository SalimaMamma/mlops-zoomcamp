if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Load the Yellow Taxi Trip Data for March 2023 from NYC TLC.
    """

    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet"
    df = pd.read_parquet(url)

    print(f"Loaded {len(df)} rows")

    return df

@test
def test_output(output, *args) -> None:
    """
    Test that the dataframe is not empty.
    """
    assert output is not None, 'The output is undefined'
    assert len(output) > 0, 'The dataframe is empty'
