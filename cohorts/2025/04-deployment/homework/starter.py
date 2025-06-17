import os
import argparse
import pickle
import pandas as pd

# Chargement du modèle et du vectorizer
with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Colonnes catégorielles utilisées pour le modèle
categorical = ['PULocationID', 'DOLocationID']

# Fonction de lecture et préparation des données
def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df

# Fonction principale exécutée par le script
def main(year, month):
    filename = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    print(f"Loading data : {year}-{month:02d}")
    df = read_data(filename)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    preds = model.predict(X_val)
    df['pred'] = preds

    print(f"Standard deviation: {df['pred'].std():.2f}")
    print(f"Mean prediction: {df['pred'].mean():.2f}")

    df_result = df[['ride_id', 'pred']]
    os.makedirs('output', exist_ok=True)

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    print(f"File saved to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True, help='Year of the data')
    parser.add_argument('--month', type=int, required=True, help='Month of the data')
    args = parser.parse_args()

    main(args.year, args.month)
