import os
import pandas as pd
from datetime import datetime
import logging


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def create_test_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    return pd.DataFrame(data, columns=columns)




def test_integration_batch_process():
    logging.basicConfig(level=logging.INFO)
    year, month = 2023, 1
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')

    
    df_input = create_test_data()

    input_file = f's3://nyc-duration/in/{year:04d}-{month:02d}.parquet'
    output_file = f's3://nyc-duration/out/{year:04d}-{month:02d}.parquet'

    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }

    
    df_input.to_parquet(input_file, engine='pyarrow', compression=None, index=False, storage_options=options)
    
    return_code = os.system(f"python batch.py {year} {month}")
    assert return_code == 0, "batch.py failed to run"
    df_result = pd.read_parquet(output_file, storage_options=options)

    logging.info(f"Sum of predicted durations: {df_result['predicted_duration'].sum():.2f}")
    


 
