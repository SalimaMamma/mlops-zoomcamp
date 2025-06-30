import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path to import batch module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    categorical = ['PULocationID', 'DOLocationID']
    
    actual_result = prepare_data(df, categorical)
    
    # Expected data after transformation:
    # Row 0: duration = 9 minutes (1:01 to 1:10) - valid
    # Row 1: duration = 8 minutes (1:02 to 1:10) - valid  
    # Row 2: duration = 59 seconds <1minutes - invalid
    # Row 3: duration = 60 minutes and 1 second > 60 minutes - invalid
    
    expected_data = [
        ('-1', '-1', dt(1, 1), dt(1, 10), 9.0),
        ('1', '1', dt(1, 2), dt(1, 10), 8.0),
    ]
    
    expected_columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)
    
    # Convert to dict for comparison
    actual_dict = actual_result.to_dict('records')
    expected_dict = expected_df.to_dict('records')
    
    assert len(actual_dict) == len(expected_dict), f"Expected {len(expected_dict)} rows, got {len(actual_dict)}"
    assert len(actual_dict) == 2, f"Expected 2 rows after filtering, got {len(actual_dict)}"
    
    # Verify the categorical columns are strings
    for row in actual_dict:
        assert isinstance(row['PULocationID'], str)
        assert isinstance(row['DOLocationID'], str)
    
    print("Test passed! Expected 2 rows in the filtered dataframe.")