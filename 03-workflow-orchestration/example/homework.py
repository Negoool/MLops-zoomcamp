import datetime
import os
import urllib
import re
import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow
from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

DATA_DIR= "./"


def get_train_val_filename(date=None):
    """Get the train and val filename based on the given date.
    If date is not given, set date to the current date.
    Get 2 months before the date as the training data, and the previous month as validation data.
    For example, if the date passed is "2021-03-15", the training data should be "fhv_tripdata_2021-01.parquet"
     and the validation file will be "fhv_trip_data_2021-02.parquet"
    """
    def go_back_by_month(input_date, delta_month):
        if input_date.month  > delta_month:
            month = input_date.month - delta_month
            year = input_date.year
        else:
            month = 12 + (input_date.month - delta_month)
            year = input_date.year - 1
        return year, month
    
    year_train, month_train = go_back_by_month(date, 2)
    train_filename = f"fhv_tripdata_{year_train}-{month_train:02d}.parquet"
    year_val, month_val = go_back_by_month(date, 1)
    val_filename = f"fhv_tripdata_{year_val}-{month_val:02d}.parquet"

    return  train_filename, val_filename

@task(retries=2)
def download_and_read_data(filename):
    logger = get_run_logger()
    local_filename = os.path.join(DATA_DIR, filename)
    if not os.path.exists(local_filename):
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"
        logger.info(f"Downloading data: {url}  ...")
        _ = urllib.request.urlretrieve(url, local_filename)
    else:
        logger.info(f"Foun {filename}  locally")
    
    logger.info(f"current working directory: {os.getcwd()}")
    logger.info(os.listdir(DATA_DIR))
    df = pd.read_parquet(local_filename)
    return df

@task
def prepare_features(df, categorical, train=True):
    logger = get_run_logger()
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@task
def train_model(df, categorical):
    logger = get_run_logger()
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")

    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return


@flow(name="homework", task_runner=SequentialTaskRunner())
def main(date_string=None):
    if date_string is None:
        date  = datetime.date.today()
        date_string = date.strftime("%Y-%m-%d")
    else:
        assert re.match(r'\d{4}-\d{2}-\d{2}', date_string)
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    train_filename, val_filename = get_train_val_filename(date)
  
    # mlflow.set_experiment("homework_03")
    # mlflow.set_tracking_uri("")
    categorical = ['PUlocationID', 'DOlocationID']

    df_train = download_and_read_data(train_filename)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = download_and_read_data(val_filename)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical)
    run_model(df_val_processed, categorical, dv, lr)


    pickle.dump(lr, open(f"model-{date_string}.bin", 'wb'))
    pickle.dump(dv, open(f"dv-{date_string}.b", 'wb'))


# main("2021-08-15")

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(main,
                        name="dpl_ct_3", 
                        schedule=CronSchedule(cron="0/5 * * * *"),
                        work_queue_name="ml_3")
deployment.apply()