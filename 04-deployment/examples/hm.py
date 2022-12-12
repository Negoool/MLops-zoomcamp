import pickle
import sys
from pathlib import Path

import pandas as pd


CATEGORICAL = ['PUlocationID', 'DOlocationID']


def read_parquete(file_path):

    df = pd.read_parquet(file_path)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    
    return df

def prepare_dict(df):
    df[CATEGORICAL] = df[CATEGORICAL].fillna(-1).astype('int').astype('str')
    dicts = df[CATEGORICAL].to_dict(orient='records')
    return dicts

def load_model(model_path="./model.bin"):
    # The model can be loaded from the mlflow artifact store, given stage or run id.
    with open(model_path, 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv,lr 
   


def run_prediction(file_name, output_file):
    # Read file
    df = read_parquete(file_name)

    # Load model
    dv, lr = load_model()

    # prepare data
    dicts = prepare_dict(df)
    
    # Make prediction
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print (y_pred.mean())

    # save the results
    predictions_df =  pd.DataFrame(y_pred, columns=["predictions"])
    predictions_df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    predictions_df.to_parquet( output_file,
        engine='pyarrow',
        compression=None,
        index=False)


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    output_location = "./outputs"

    file_path = f"https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{year:4d}-{month:02d}.parquet"

    file_name = Path(file_path).name

    Path(output_location).mkdir(parents=True, exist_ok=True)

    run_prediction(file_path, Path(output_location) / file_name)



    




