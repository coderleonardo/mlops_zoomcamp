import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    mlflow.set_experiment("experiment-1")
    with mlflow.start_run():

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        max_depth = 10
        mlflow.log_params({"max_depth": max_depth})
        rf = RandomForestRegressor(max_depth=max_depth, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse_on_val_data", rmse)

        mlflow.sklearn.log_model(rf, artifact_path="models")
        print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


if __name__ == '__main__':
    run_train()
