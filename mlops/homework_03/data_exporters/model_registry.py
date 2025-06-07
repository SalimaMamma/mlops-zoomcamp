if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import mlflow
import mlflow.sklearn
import pickle

@data_exporter
def export_model(output, *args, **kwargs):
    dv, model = output

    mlflow.set_tracking_uri("file:///home/src/mlruns")
    mlflow.set_experiment("nyc_taxi_experiment")

    with mlflow.start_run():
       
        with open("dict_vectorizer.b", "wb") as f_out:
            pickle.dump(dv, f_out)

      
        mlflow.sklearn.log_model(model, "model_logg")
        mlflow.log_param("model_type", "LinearRegression")

       
        mlflow.log_artifact("dict_vectorizer.b", artifact_path="artifacts")
